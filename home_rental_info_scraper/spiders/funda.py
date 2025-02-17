import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
# from models.Home import Home
# from utils import util
# from services.home_services import get_unique_home_list,save_new_homes

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
                    PageMethod("wait_for_selector", "div.gap-3", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
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
            
            print("\n--------------------------")
            print(f"url : {url}")
            print(f"image_Url = {image_url}")
            print(f"address : {address}")
            print(f"price : {price}")
            print(f"Name : {agency}")
            print("--------------------------\n")
            
        #     home = Home(
        #         url=url,
        #         image_url=image_url,
        #         address=address,
        #         price=price,
        #         agency=agency
        #     )
        #     parsed_home_list.append(home)
        
        # unique_home_list = get_unique_home_list(parsed_home_list)
        # if save_new_homes(unique_home_list):
        #     print(f"New home list uploaded to the db storage")
        # else:
        #     print(f"Something went wrong while trying to saving the home list to the db.")
            
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
            


