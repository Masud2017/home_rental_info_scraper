import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string


class ParariusSpider(scrapy.Spider):
    name = "pararius"
    allowed_domains = ["pararius.nl"]
    start_urls = ["https://www.pararius.nl/huurwoningen/nederland"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "li.search-list__item", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        try:
            page = response.meta["playwright_page"]
        
            while True:
                data = await page.content()
                home_card_list = Selector(text=data).xpath("//li[contains(@class , 'search-list__item search-list__item--listing')]")

                # await page.wait_for_selector("//a[contains(@class, 'propertyLink')]", timeout=6000)

                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    url_portion = home_card.xpath(".//div[contains(@class,  'listing-search-item__depiction')]/a").attrib['href']
                    if url_portion is not None:
                        url = self.allowed_domains[0] + url_portion
                    url = self.allowed_domains[0]
                    image_url = home_card.xpath(".//div[contains(@class,  'listing-search-item__depiction')]/a/wc-picture/picture/img").get()
                    if image_url is not None:
                        reg = r'src="([^"]+)"'
                        search = re.search(reg, image_url)
                        if search:
                            image_url = search.group(1)
                    
                    city = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//div[contains(@class ,'listing-search-item__sub-title')]/text()").get().strip()
                    
                    
                    if city is None:
                        city = ""
                    if city is not None:
                        city = parse_city_string(city)
                    address = ""
                    address = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//h2[contains(@class,'listing-search-item__title')]/a/text()").get().strip()
                    if address is not None:
                        address = address + "," + city
                    price = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//div[contains(@class ,'listing-search-item__price')]/text()").get().strip()
                    print(f"Debugging the price {price}")
                    price = price.split(" ")[0]
                    if len(price) > 0:
                        print(f"Yoyuo")
                        price = price.strip()
                        price = price[2:]
                    agency = self.name
                    room_count = home_card.xpath(".//ul[contains(@class, 'illustrated-features illustrated-features--compact')]/li[2]/text()").get()
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[0]
                    else:
                        room_count = "1"
                    
                    print("\n--------------------------")
                    print(f"url : {url}")
                    print(f"image_Url = {image_url}")
                    print(f"address : {address}")
                    print(f"city : {city}")
                    print(f"price : {price}")
                    print(f"Name : {agency}")
                    print(f"Room count : {room_count}")
                    print("--------------------------\n")
                    home = Home(
                        address=address,
                        city=city,
                        url=url,
                        agency=agency,
                        price=price,
                        image_url=image_url,
                        room_count=room_count
                    )
                    yield HomeRentalInfoScraperItem(home=home)
                    
                    
                has_next = response.meta["playwright_page"].locator("//a[contains(@class, 'pagination__link pagination__link--next')]")
                print(f"debugging the next page : {has_next}")
                    
                if await has_next.is_visible():
                    # cls_next = await has_next.get_attribute("class")
                    # print(f"debugging the next page : {cls_next}")
                    # if cls_next == "active active-exact pagination__arrow pagination__next icon-caret-right":
                    await has_next.click()
                    await response.meta["playwright_page"].wait_for_selector("li.search-list__item")  # Wait for new cards
                else:
                    break
                
        except Exception as e:
            print(f"Error while parsing: {e}")
