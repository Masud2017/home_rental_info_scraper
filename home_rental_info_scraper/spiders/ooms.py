import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re

class OomsSpider(scrapy.Spider):
    name = "ooms"
    allowed_domains = ["ooms.com"]
    start_urls = ["https://ooms.com/wonen/aanbod"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.card--object--properties", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'card card--default card--object card--object--properties')]")
        

        print(f"count of home list : {len(home_card_list)}")
        for home_card in home_card_list:
            url = self.allowed_domains[0] + home_card.xpath("./a").attrib['href']
        #     image_url = self.allowed_domains[0] + home_card.xpath(".//div[contains(@class,  'property__image-container')]//div[contains(@class, 'property__image')]").get()
        #     # with open("log.txt", "w", encoding = "utf-8") as f:
        #     #     f.write(image_url)
        #     # image_url = re.search(r"background-image:\s*url\(&quot;(.*?)&quot;\);",image_url).group(1)
            city = ""
            city = home_card.xpath(".//div[contains(@class, 'card--default__content')]//div[contains(@class, 'card--default__body')]/h5/text()").get()
            address = ""
            address = city + "," +  (home_card.xpath(".//div[contains(@class, 'card--default__content')]//div[contains(@class, 'card--default__body')]/small/text()").get()) 
            price = home_card.xpath(".//div[contains(@class, 'card--default__content')]//footer[contains(@class, 'card--default__footer')]/strong/text()").get()
            splitted_price = price.split(" ")
            if (len(splitted_price) > 0):
                price = splitted_price[1]
                price = splitted_price[1]
            agency = self.name
            
            print(f"url : {url}")
            # print(f"image_Url = {image_url}")
            print(f"address : {address}")
            print(f"price : {price}")
            print(f"Name : {agency}")
            # 
        #     # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
            
        #     has_next = response.meta["playwright_page"].locator("//li[contains(@class, 'pagination-item')]/button[contains(@aria-label, 'Go to next page')]")
            
            
           
        # if await has_next.is_visible():
        #     await has_next.click()
        #     await response.meta["playwright_page"].wait_for_selector("div.property-cards__single")  # Wait for new cards
        #     yield scrapy.Request(
        #         response.url,
        #         meta={"playwright": True, "playwright_include_page": True},
        #         callback=self.parse
        #     )
            
            
            
# properties that need to be extracted          
# url
# home_url
# city
# address
# price
# agency
        

