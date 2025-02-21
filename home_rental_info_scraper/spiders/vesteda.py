import scrapy
import asyncio
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem

class VestedaSpider(scrapy.Spider):
    name = "vesteda"
    allowed_domains = ["www.vesteda.com"]
    start_urls = ["https://www.vesteda.com/nl/woning-zoeken?placeType=0&sortType=0&radius=20&s=&sc=woning&latitude=0&longitude=0&filters=0&priceFrom=500&priceTo=9999"]
    
# //div[contains(@class, 'o-card--listview-container')]
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.o-card--listview-container", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'o-card--listview-container')]")
        print(f"Total Home Cards : {len(home_card_list)}")
        for home_card in home_card_list:
            url = self.allowed_domains[0] + home_card.xpath(".//a").attrib['href']
            await page.wait_for_selector("//div[contains(@class, 'o-card--listview-image')]/picture/img", timeout=6000)

            image_url = home_card.xpath("//div[contains(@class, 'o-card--listview-image')]/picture/source").attrib['data-srcset']
            city = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-reorder-column__first')]/strong/text()").get()
            address = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//h3[contains(@class, 'h4 u-margin-bottom-none')]/span/text()").get() + ","+ city
            price = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-card--listview-price')]/b[contains(@class, 'h5')]/text()").get()
            agency = "Vesteda"
            room_count = home_card.xpath(".//ul[contains(@class, 'o-layout o-layout-gap o-layout--gutter-tiny')]/li[2]/b/text()").get()
            if room_count is not None:
                room_count = room_count.strip()
                room_count = room_count.split(" ")[0]
            else:
                room_count = "1"
            # date_added = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-card--listview-price')]/text()").get()
            
            print(f"url : {url}")
            print(f"image url : {image_url}")
            print(f"city : {city}")
            print(f"address: {address}")
            print(f"price : {price}")
            print(f"agency : {agency}")
            print(f"room_count : {room_count}")
            
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