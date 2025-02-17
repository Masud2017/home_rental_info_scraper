import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector


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
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//li[contains(@class , 'search-list__item search-list__item--listing')]")

        # await page.wait_for_selector("//a[contains(@class, 'propertyLink')]", timeout=6000)

        print(f"count of home list : {len(home_card_list)}")
        for home_card in home_card_list:
            url = self.allowed_domains[0] + home_card.xpath(".//div[contains(@class,  'listing-search-item__depiction')]/a").attrib['href']
            # image_url = home_card.xpath(".//div[contains(@class,  'listing-search-item__depiction')]/a/wc-picture/picture/img").attrib["src"]
            
            city = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//div[contains(@class ,'listing-search-item__sub-title')]/text()").get().strip()
            
            
            if city is None:
                city = ""
            address = "" + city
            address = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//h2[contains(@class,'listing-search-item__title')]/a/text()").get().strip() + "," + city
            price = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//div[contains(@class ,'listing-search-item__price')]/text()").get().strip()
            print(f"Debugging the price {price}")
            price = price.split(" ")[0]
            if len(price) > 0:
                print(f"Yoyuo")
                price = price.strip()
                price = price[2:]
            agency = self.name
            
            print("\n--------------------------")
            print(f"url : {url}")
            # print(f"image_Url = {image_url}")
            print(f"address : {address}")
            print(f"price : {price}")
            print(f"Name : {agency}")
            print("--------------------------\n")
            
            
            # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
            
        # has_next = response.meta["playwright_page"].locator("//ul[contains(@class, 'pagination')]//li[last()]")
            
            
           
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
            

