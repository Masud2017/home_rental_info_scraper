import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem

class FundaSpider(scrapy.Spider):
    name = "funda"
    allowed_domains = ["www.funda.nl"]
    start_urls = ["https://www.funda.nl/zoeken/huur"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.gap-3", timeout=6000),
                    # PageMethod("evaluate", "window.scrollBy(0,100)"),
                    # PageMethod("click", "//div[contains(@class,'multiple didomi-buttons didomi-popup-notice-buttons')]/button[3]")
                ],
            },
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
        }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'flex flex-col gap-3 mt-4')]/div")
        # parsed_home_list = list()

        print(f"count of home list : {len(home_card_list)}")
        for home_card in home_card_list:
            url = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a").attrib['href']
            print(f"Debugging the value of url : {url}")
            image_url = home_card.xpath(".//div[contains(@class, 'relative items-center justify-center sm:flex')]/a/div/img").attrib["srcset"].split(" ")[0]
            
            
            city = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[2]/text()").get().strip()
            # debugging purpose only
            # print(f"debugging the value of city : {home_card.xpath("//a[contains(@class, 'propertyLink')]/figure/figcaption/span[1]").get()}")
            
            if city is None:
                city = ""
            address = "" + city
            address = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]/h2/a//div[contains(@class,  'flex font-semibold')]/span[1]/text()").get().strip() + "," + city
            price = home_card.xpath(".//div[contains(@class, 'relative flex w-full min-w-0 flex-col pl-0 pt-4 sm:pl-4 sm:pt-0')]//div[contains(@class, 'font-semibold mt-2')]/div[2]/text()").get()
            if price is not None:
                price = price.split(" ")[1:-1]
            agency = self.name
            room_count = home_card.xpath(".//div[contains(@class, 'flex space-x-3')]/ul/li[2]/span[2]/text()").get()
            if room_count is not None:
                room_count = room_count.strip()
            
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