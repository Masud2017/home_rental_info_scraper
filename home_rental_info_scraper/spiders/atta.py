import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.models.Home import Home

class AttaSpider(scrapy.Spider):
    name = "atta"
    allowed_domains = ["atta.nl"]
    start_urls = ["https://atta.nl/woningaanbod/huuraanbod/"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.object-list__wrapper", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'list__objects')]//div[contains(@class, 'tabsList list__container')]//div[contains(@class, 'list__object')]")
        # with open('log.txt', 'a', encoding='utf-8') as f:
        #     f.write(str(len(home_card_list)))

        print(f"count of home list : {len(home_card_list)}")
        for home_card in home_card_list:
            url = home_card.xpath("./a").attrib['href']
            image_url = home_card.xpath(".//div[contains(@class, 'object-list__wrapper')]//div[contains(@class, 'object-list__media')]/figure/img").attrib["src"]
            # # with open("log.txt", "w", encoding = "utf-8") as f:
            # #     f.write(image_url)
            # # image_url = re.search(r"background-image:\s*url\(&quot;(.*?)&quot;\);",image_url).group(1)
            city = ""
            city = home_card.xpath(".//div[contains(@class, 'object-list__wrapper')]/div[2]/div[1]/div[contains(@class, 'object-list__city')]/text()").get()
            address = ""
            address = (home_card.xpath(".//div[contains(@class, 'object-list__wrapper')]/div[2]/div[1]/div[contains(@class, 'object-list__address')]/text()").get()) + "," + city
            price = home_card.xpath(".//div[contains(@class, 'object-list__wrapper')]/div[2]/div[1]/div[contains(@class, 'object-list__price')]/text()").get()
            if price is not None:
                price = price.split(" ")[1]
            agency = self.name
            room_count = home_card.xpath(".//div[contains(@class, 'object-list__wrapper')]/div[2]/div[1]/div[contains(@class, 'object-list__area')]/span[3]/text()").get()
            if room_count is not None:
                room_count = room_count.strip()
                room_count = room_count.split(" ")[0]

            
            print(f"url : {url}")
            print(f"image_Url = {image_url}")
            print(f"address : {address}")
            print(f"city : {city}")
            print(f"price : {price}")
            print(f"Name : {agency}")
            print(f"Room count : {room_count}")
            
            home = Home(
                address=address,
                city=city,
                url=url,
                agency=agency,
                price=price,
                image_url=image_url,
                room_count=room_count
            )
            item = HomeRentalInfoScraperItem()
            item["home"] = home
            yield item
            
            # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
            
            # has_next = response.meta["playwright_page"].locator("//li[contains(@class, 'pagination-item')]/button[contains(@aria-label, 'Go to next page')]")
            
            
           
        # if await has_next.is_visible():
        #     await has_next.click()
        #     await response.meta["playwright_page"].wait_for_selector("div.property-cards__single")  # Wait for new cards
        #     yield scrapy.Request(
        #         response.url,
        #         meta={"playwright": True, "playwright_include_page": True},
        #         callback=self.parse
        #     )
            