import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
import asyncio
from home_rental_info_scraper.models.Home import Home
from ..items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string
import traceback


class WoonzekerSpider(scrapy.Spider):
    name = "woonzeker"
    allowed_domains = ["woonzeker.com"]
    start_urls = ["https://woonzeker.com/aanbod"]
    home_list = list()

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.property.offer-card", timeout=6000)
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
                home_card_list = Selector(text=data).xpath("//div[contains(@class, 'property offer-card')]")
                with open('log.txt', 'a', encoding='utf-8') as f:
                    f.write(str(len(home_card_list)))

                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    url = "https://"+self.allowed_domains[0] + home_card.xpath("./a").attrib['href']
                    image_url = home_card.xpath(".//div[contains(@class, 'offer-card__image')]//div[contains(@class,'property-images')]//div[contains(@class, 'gallery')]//div[contains(@class, 'q-carousel q-panel-parent q-carousel--without-padding gallery')]//div[contains(@class, 'q-carousel__slides-container')]//div[contains(@class ,'q-panel scroll')]//div[contains(@class,'q-carousel__slide asset-image')]/img").attrib["src"]
                    # regex_image_url = r'background-image:\s*url\(["\']?(.*?)["\']?\);'
                    # if image_url is not None:
                    #     print(f"printing the image url : {image_url}")
                    #     res = re.search(regex_image_url,image_url)
                    #     if res is not None:
                    #         image_url = res.group(1)
                    #     else:
                    #         image_url = ""
                    
                    city = ""
                    city = home_card.xpath(".//div[contains(@class , 'offer-card__content')]/div/div[1]/text()").get()
                    address = ""
                    if city is not None:
                        address = (home_card.xpath(".//div[contains(@class , 'offer-card__content')]/h1/text()").get()) + ","+city
                        city = parse_city_string(city)
                        if "\'" in city:
                            city = city.replace("\'", "")
                        
                    price = home_card.xpath(".//div[contains(@class , 'offer-card__content')]/div/b/text()").get()
                    if price is not None:
                        price = price.split(" ")[1]
                        price = price.replace(".", "")
                    else:
                        price = "0"
                        
                    agency = self.name
                    room_count = home_card.xpath(".//div[contains(@class , 'offer-card__content')]/div/div[2]/span[last()]/text()").get()
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[0]
                    
                    print(f"url : {url}")
                    print(f"image_Url = {image_url}")
                    print(f"address : {address}")
                    print(f"city : {city}")
                    print(f"price : {price}")
                    print(f"Name : {agency}")
                    print(f"Room count : {room_count}")
                    home = Home(address, city=city, url = url, agency = agency, price = price,image_url = image_url,room_count=room_count)
                    # self.home_list.append(home)
                    
                    item = HomeRentalInfoScraperItem()
                    item["home"] = home
                    yield item
                    # yield HomeRentalInfoScraperItem()
                    
                    # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
                    
                has_next = response.meta["playwright_page"].locator("//button[contains(@aria-label, 'Go to next page')]")
                disabled_var = await has_next.get_attribute("disabled")
                print(f"Debugging the attribute from locator : {disabled_var}")
                if (disabled_var != "disabled"):
                
                    if await has_next.is_visible():
                        await has_next.click()
                        await response.meta["playwright_page"].wait_for_selector("div.property.offer-card")  # Wait for new cards
                    
                else:
                    break

        except Exception as e:
            print(f"Error while parsing : {e}")
            traceback.print_exc()
