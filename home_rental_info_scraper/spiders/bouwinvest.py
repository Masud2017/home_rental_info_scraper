import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string
import random
import traceback
import time


class BouwinvestSpider(scrapy.Spider):
    name = "bouwinvest"
    allowed_domains = ["www.wonenbijbouwinvest.nl"]
    start_urls = ["https://www.wonenbijbouwinvest.nl/huuraanbod?query=&range=&price=&type=&availability=&orientation=&sleepingrooms=&surface="]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.projectproperty-tile", timeout=6000)
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
                home_card_list = Selector(text=data).xpath("//div[contains(@class, 'projectproperty-tile box-shadow')]")

                # await page.wait_for_selector("//a[contains(@class, 'propertyLink')]", timeout=6000)

                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    url = home_card.xpath("./a").attrib['href']
                    image_url = home_card.xpath(".//span[contains(@class, 'd-block col-12 col-lg-4')]/span[1]/span[1]/span[1]/span[1]").get()
                    image_regex = r'background-image:\s*url\("([^"]+)"\)'
                    if image_url is not None:
                        image_url = re.search(image_regex, image_url).group(1)
                    
                    city = home_card.xpath(".//span[contains(@class, 'projectproperty-tile__content__header relative')]/span[1]/text()").get().strip()
                    
                    if city is None:
                        city = ""
                    address = "" + city
                    if city is not None:
                        address = home_card.xpath(".//span[contains(@class, 'projectproperty-tile__content__body')]/span[1]/text()").get().strip() + "," + city
                        city = parse_city_string(city)
                    price = home_card.xpath(".//span[contains(@class, 'projectproperty-tile__content__footer__prices text-center text-lg-right d-flex flex-column-reverse flex-lg-column')]/span[2]/text()").get()
                    if price is not None:
                        price = price.split(" ")[1:-1][0]
                        if "." in price:
                            price = price.replace(".", "")
                        if "," in price:
                            price = price.replace(",", ".")
                    
                    agency = self.name
                    
                    room_count = home_card.xpath(".//span[contains(@class, 'projectproperty-tile__content__footer__facets d-flex')]/span[3]/text()").get()
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[0]
                    
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
                        url=url,
                        image_url=image_url,
                        address=address,
                        price=price,
                        agency=agency,
                        room_count=room_count
                    )
                    item = HomeRentalInfoScraperItem()
                    item["home"] = home
                    yield item
                
                await page.wait_for_timeout(random.randint(3000, 5000))    
                has_next = response.meta["playwright_page"].locator("a.active.active-exact.pagination__arrow.pagination__next.icon-caret-right")
                print(f"Debugging the has next page for potential anomalies : {has_next}")
                
                if await has_next.is_visible():
                    href_link = Selector(text = data).css("a.active.active-exact.pagination__arrow.pagination__next.icon-caret-right").attrib["href"]   
                    print(f"Debugging the href link : {href_link}")
                    
                    
                    cls_next = await has_next.get_attribute("class")
                    print(f"debugging the next page : {cls_next}")
                    if cls_next == "active active-exact pagination__arrow pagination__next icon-caret-right":
                        await page.wait_for_timeout(3000)
                        try:
                            await has_next.click()
                        except Exception as e:
                            print(f"Error while clicking the next page : {e}")
                            
                            print(f"Got an error while clicking the next page so retrying for one last time")
                            await page.goto("https://www.wonenbijbouwinvest.nl/"+href_link)
                        
                        
                        # try:
                        #     await response.meta["playwright_page"].wait_for_selector("div.projectproperty-tile")  # Wait for new cards
                        # except Exception as e:
                        #     print(f"Faced an issue while searching for projectproperty-tile so retrying for one last time : {e}")
                        #     await response.meta["playwright_page"].wait_for_selector("div.projectproperty-tile")  # Wait for new cards
                        
                else:
                    break
        except Exception as e:
            print(f"Error while parsing : {e}")
            traceback.print_exc()
            