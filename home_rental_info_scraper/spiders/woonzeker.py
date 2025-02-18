import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
import asyncio
from home_rental_info_scraper.models.Home import Home
from ..items import HomeRentalInfoScraperItem
# from home_rental_info_scraper.models.Home import Home


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
                    PageMethod("wait_for_selector", "div.property-cards__single", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        while True:
            data = await page.content()
            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'property-cards__single')]")
            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write(str(len(home_card_list)))

            print(f"count of home list : {len(home_card_list)}")
            for home_card in home_card_list:
                url = "https://"+self.allowed_domains[0] + home_card.xpath(".//div[contains(@class,'property__body-container')]/a").attrib['href']
                image_url = home_card.xpath(".//div[contains(@class,  'property__image-container')]//div[contains(@class, 'property__image')]").get()
                regex_image_url = r'background-image:\s*url\(["\']?(.*?)["\']?\);'
                if image_url is not None:
                    print(f"printing the image url : {image_url}")
                    res = re.search(regex_image_url,image_url)
                    if res is not None:
                        image_url = res.group(1)
                    else:
                        image_url = ""
                # with open("log.txt", "w", encoding = "utf-8") as f:
                #     f.write(image_url)
                # image_url = re.search(r"background-image:\s*url\(&quot;(.*?)&quot;\);",image_url).group(1)
                city = ""
                city = home_card.xpath(".//div[contains(@class, 'property__body-container')]//h1/text()").get()
                address = ""
                address = city + "," +  (home_card.xpath(".//div[contains(@class, 'property__body-container')]//div[contains(@class , 'property__location')]/span[1]/text()").get() + home_card.xpath(".//div[contains(@class, 'property__body-container')]//div[contains(@class , 'property__location')]/span[2]/text()").get()) 
                price = home_card.xpath(".//div[contains(@class, 'property__price')]/span[2]/text()").get()
                price = price.split(",")[0]
                price = price.split(" ")[1]
                agency = self.name
                
                print(f"url : {url}")
                print(f"image_Url = {image_url}")
                print(f"address : {address}")
                print(f"price : {price}")
                print(f"Name : {agency}")
                home = Home(address, city=city, url = url, agency = agency, price = price,image_url = image_url)
                # self.home_list.append(home)
                
                item = HomeRentalInfoScraperItem()
                item["home"] = home
                yield item
                # yield HomeRentalInfoScraperItem()
                
                # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
                
            has_next = response.meta["playwright_page"].locator("//li[contains(@class, 'pagination-item')]/button[contains(@aria-label, 'Go to next page')]")
            disabled_var = await has_next.get_attribute("disabled")
            print(f"Debugging the attribute from locator : {disabled_var}")
            if (disabled_var != "disabled"):
            
                if await has_next.is_visible():
                    await has_next.click()
                    await response.meta["playwright_page"].wait_for_selector("div.property-cards__single")  # Wait for new cards
                
            else:
                break

            
# reference          
 # await self.parse(
                #     scrapy.http.Response(
                #         url=response.url,
                #         request=response.request,
                #         # meta={"playwright_page": page},
                #     )
                # )
            #     yield scrapy.Request(
            #     url=response.url,
            #     meta={
            #         "playwright": True,
            #         "playwright_include_page": True,
            #         "playwright_page_methods": [
            #             PageMethod("wait_for_selector", "div.property-cards__single", timeout=6000)
            #         ],
            #     },
            #     headers = {
            #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            #     },
            #     callback=self.parse
                
            # )