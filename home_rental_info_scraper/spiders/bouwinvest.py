import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
from home_rental_info_scraper.models.Home import Home


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
        home_list = list()
        page = response.meta["playwright_page"]
        
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
            address = home_card.xpath(".//span[contains(@class, 'projectproperty-tile__content__body')]/span[1]/text()").get().strip() + "," + city
            price = home_card.xpath(".//span[contains(@class, 'projectproperty-tile__content__footer__prices text-center text-lg-right d-flex flex-column-reverse flex-lg-column')]/span[2]/text()").get()
            price = price.split(" ")[1:-1][0]
            
            agency = self.name
            
            print("\n--------------------------")
            print(f"url : {url}")
            print(f"image_Url = {image_url}")
            print(f"address : {address}")
            print(f"price : {price}")
            print(f"Name : {agency}")
            print("--------------------------\n")
            
            home = Home(
                url=url,
                image_url=image_url,
                address=address,
                price=price,
                agency=agency
            )
            
            
            home_list.append(home)
            
            
            # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
            
        # has_next = response.meta["playwright_page"].locator("//ul[contains(@class, 'pagination')]//li[last()]")
        yield home_list
            
            
           
        # if await has_next.is_visible():
        #     await has_next.click()
        #     await response.meta["playwright_page"].wait_for_selector("div.col-lg-4")  # Wait for new cards
        #     yield scrapy.Request(
        #         response.url,
        #         meta={"playwright": True, "playwright_include_page": True},
        #         headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        #         },
        #         callback=self.parse
        #     )
        # else:
        #     print("All the pages finished scraping")
            

