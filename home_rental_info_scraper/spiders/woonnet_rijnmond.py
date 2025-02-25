import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
from home_rental_info_scraper.models.Home import Home
from ..items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string

class WoonnetRijnmondSpider(scrapy.Spider):
    name = "woonnet_rijnmond"
    allowed_domains = ["www.woonnetrijnmond.nl"]
    start_urls = ["https://www.woonnetrijnmond.nl/"]

    
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.js-animate-fadein", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def scroll(self,home_card_list,page,data):
        while True:
            prev_count = len(home_card_list)
            await page.evaluate("window.scrollBy(0,document.body.scrollHeight)")
            data = await page.content()
            # import time
            # time.sleep(10)
            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'js-animate-fadein')]")
            # await page.wait_for_selector("div.js-animate-fadein", timeout=6000)
            print(len(home_card_list))
            if (len(home_card_list) > prev_count):
                continue
            else:
                return home_card_list
                
    async def parse(self, response):
        try:
            page = response.meta["playwright_page"]
        
            data = await page.content()
            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'js-animate-fadein')]")
            home_card_list = await self.scroll(home_card_list,page,data)
            print(f"Printing the home_card_list: {len(home_card_list)}")
            
            # with open("log.txt", "a") as f:
            #         f.write(''.join(home_card_list.getall()))
            print(f"Total Home Cards : {len(home_card_list)}")
            for home_card in home_card_list:
                url = self.allowed_domains[0] + home_card.xpath(".//a").attrib['href']
                # await page.wait_for_selector("div['data-size-desktop']", timeout=6000)
                
                

                image_url = home_card.xpath(".//div[contains(@class, 'swipe__list')]//div[contains(@class, 'swipe__item')][1]//div[contains(@class, 'swipe__image')]").get()
                regex = r"background-image:url\(['\"]?(.*?)['\"]?\)"
                image_url = re.search(regex, image_url).group(1)
                if (len(image_url) > 2):
                    image_url = image_url[2:]
                    
                city = home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box__properties')]//div[contains(@class, 'box__title')][2]/span/text()").get().strip()
                address = ""
                if city is not None:
                    address = home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box__properties')]//div[contains(@class, 'box__title')][1]/text()").get().strip()
                    if address is not None:
                        address = address + ","+ city
                    else:
                        address = city
                    if parse_city_string(city) is not None:
                        city = parse_city_string(city)
                    
                price = home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box--obj__price')]/text()").get()
                if price is not None:
                    price = price[2:]
                    if "." in price:
                        price = price.replace(".", "")
                    if "," in price:
                        price = price.replace(",", ".")
                agency = self.name
                room_count = home_card.xpath(".//div[contains(@class, 'box__text  ellipsis')]/text()").get()
                if room_count is not None:
                    room_count = room_count.strip()
                    room_count = room_count.split(" ")[0]
                # date_added = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-card--listview-price')]/text()").get()
                
                print(url)
                print(f"image url : {image_url}")
                print(f"city : {city}")
                print(f"address: {address}")
                print(f"price : {price}")
                print(f"agency : {agency}")
                print(f"room count : {room_count}")
                home = Home(address, city=city, url = url, agency = agency, price = price,image_url = image_url,room_count=room_count)
                item = HomeRentalInfoScraperItem()
                item["home"] = home
                yield item
        except Exception as e:
            print(f"Error while parsing: {e}")