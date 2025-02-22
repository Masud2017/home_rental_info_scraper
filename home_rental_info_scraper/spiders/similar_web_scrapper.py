import scrapy
import asyncio
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
from ..items import HomeRentalInfoScraperItem

class SimilarWebScrapper(scrapy.Spider):
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.list-item-content", timeout=6000)
                ],
                # "page_number": 1
            },
            # headers ={}
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'list-item-content')]")
        print(len(home_card_list))
        for home_card in home_card_list:
            image_url = self.allowed_domains[0] + home_card.xpath(".//img/@src").get()
            street = home_card.xpath(".//div[contains(@class, 'object-address')]/span[1]/span/text()").get()
            address = street + home_card.xpath(".//div[contains(@class, 'object-address')]/span[1]/text()").get()
            city = home_card.xpath(".//div[contains(@class, 'object-address')]//span[contains(@class, 'address-part')][2]/text()").get()
            agency = self.name
            price = home_card.xpath(".//span[contains(@class, 'kosten-regel2')]/text()").get()
            if price is not None:
                price = price.split(" ")
                if len(price) > 1:
                    price = price[2][2:]
                    # CONVERTING FROM EUROPEAN FORMAT TO AMERICAN FORMAT (CURRENCY)
                    if "," in price:
                        price = price.replace(",", ".")
                    if "." in price:
                        price = price.replace(".", "")
            url = self.allowed_domains[0] + home_card.xpath(".//a[contains(@ng-click,'goToDetails')]").attrib['href']
            
            print(f"Image : {image_url}")
            print(f"Price : {price}")
            print(f"Address : {address}")
            print(f"URL : {url}")
            print(f"City : {city}")
            print(f"Agency : {agency}")            
            
            home = Home(
                image_url=image_url,
                address=address,
                city=city,
                agency=agency,
                price=price,
                url=url
            )
            yield HomeRentalInfoScraperItem(home=home)
    