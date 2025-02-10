import scrapy
import asyncio
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector


class AntaresSpider(scrapy.Spider):
    name = "antares"
    allowed_domains = ["wonen.thuisbijantares.nl"]
    start_urls = ["https://wonen.thuisbijantares.nl/aanbod/nu-te-huur/te-huur"]

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
            image_link = self.allowed_domains[0] + home_card.xpath(".//img/@src").get()
            street = home_card.xpath(".//div[contains(@class, 'object-address')]/span[1]/span/text()").get()
            address = street + home_card.xpath(".//div[contains(@class, 'object-address')]/span[1]/text()").get()
            price = home_card.xpath(".//span[contains(@class, 'kosten-regel2')]/text()").get()
            url = self.allowed_domains[0] + home_card.xpath(".//a[contains(@ng-click,'goToDetails')]").attrib['href']
            
            print(f"Image : {image_link}")
            print(f"Price : {price}")
            print(f"Address : {address}")
            print(f"URL : {url}")
            
    
