import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string

class NmgSpider(scrapy.Spider):
    name = "nmg"
    allowed_domains = ["nmgwonen.nl"]
    start_urls = ["https://nmgwonen.nl/woningen"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "article.house", timeout=6000)
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
                home_card_list = Selector(text=data).xpath("//article[contains(@class, 'house huur')]")

                # await page.wait_for_selector("//a[contains(@class, 'propertyLink')]", timeout=6000)

                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    url = home_card.xpath("./a").attrib['href']
                    image_url = home_card.xpath(".//figure[contains(@class, 'house__figure')]/img").get()
                    if image_url is not None:
                        reg = r'data-lazy-srcset="([^"]+)"'
                        alternate_reg = r'src="([^"]+)"'
                        search = re.search(reg, image_url)
                        if search:
                            image_url = search.group(1)
                            image_url = image_url.split(",")[0].split(" ")[0]
                        else:
                            search = re.search(alternate_reg, image_url)
                            if search:
                                image_url = search.group(1)
                    city = home_card.xpath(".//div[contains(@class, 'house__content')]//div[contains(@class, 'house__heading heading u-center')]/h2/span/text()").get().strip()
                    # debugging purpose only
                    # print(f"debugging the value of city : {home_card.xpath("//a[contains(@class, 'propertyLink')]/figure/figcaption/span[1]").get()}")
                    
                    if city is None:
                        city = ""
                    address = "" + city
                    if city is not None:
                        address = home_card.xpath(".//div[contains(@class, 'house__content')]//div[contains(@class, 'house__heading heading u-center')]/h2/text()").get().strip() + "," + city
                        city = parse_city_string(city)
                        
                    price = home_card.xpath(".//div[contains(@class, 'house__content')]//div[contains(@class, 'house__listing')]/ul/li[1]/span[2]/text()").get()
                    if price is not None:
                        price = price.split(" ")[1]
                        price = price.split(",")[0]
                        price = price.replace(".","")
                        price = price.replace(",",".")
                    else:
                        price = "0"
                    agency = self.name
                    room_count = home_card.xpath("//ul[contains(@class ,'house__list u-center')]/li[last()]/span[2]/text()").get()
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[0]
                    else:
                        room_count = 1
                    
                    print("\n--------------------------")
                    print(f"url : {url}")
                    print(f"image_Url = {image_url}")
                    print(f"address : {address}")
                    print(f"City : {city}")
                    print(f"price : {price}")
                    print(f"Name : {agency}")
                    print(f"Room count : {room_count}")
                    print("--------------------------\n")
                    
                    home = Home(
                            url=url,
                            city = city,
                            image_url=image_url,
                            address=address,
                            price=price,
                            agency=agency,
                            room_count=room_count
                        )
                    item = HomeRentalInfoScraperItem()
                    item["home"] = home
                    yield item
                        
                has_next = response.meta["playwright_page"].locator("a.next.page-numbers")
                
                if await has_next.is_visible():
                    await has_next.click()
                    await response.meta["playwright_page"].wait_for_selector("article.house")  # Wait for new cards
                else:
                    break
                    
        except Exception as e:
            print(f"Error while parsing : {e}")