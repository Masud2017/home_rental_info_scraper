import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import random
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string
import traceback

class OomsSpider(scrapy.Spider):
    name = "ooms"
    allowed_domains = ["ooms.com"]
    # start_urls = ["https://ooms.com/wonen/aanbod"]
    start_urls = ["https://ooms.com/wonen/aanbod?buy_rent=rent&order_by=created_at-desc"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.card--object--properties", timeout=6000),
                    PageMethod("click", "//div[contains(@id,'CybotCookiebotDialogFooter')]//button[contains(@id, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')]" , timeout=15000),
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )


    def slow_scroll_js(self):
        return f"""
        async () => {{
            const scrollableDiv = true;
            if (scrollableDiv) {{
                var totalHeight = document.body.scrollHeight;
                const step = totalHeight / 10; // Divide the scroll into 10 steps
                let currentPosition = 0;
                
                while (currentPosition < totalHeight) {{
                    currentPosition += step;
                    window.scrollBy(0, step/0.5);
                    await new Promise(resolve => setTimeout(resolve, 200));
                    
                    if (totalHeight < document.body.scrollHeight) {{
                        totalHeight = document.body.scrollHeight;
                    }}
                }}
            }} else {{
                console.error('Scrollable element not found!');
            }}
        }}
        """
        
    async def scroll(self,home_card_list,page,data):
        while True:
            await page.evaluate("window.scrollBy(0,-document.body.scrollHeight)")
            total_pagination = r"//div[contains(@class, 'pagination__total')]/span/text()"
            total_pagination_selector = Selector(text=data).xpath(total_pagination).get()
            currently_loaded = 0
            total = 0
            if total_pagination_selector is not None:
                print(f"Total pagination : {total_pagination_selector}")
                currently_loaded = int(total_pagination_selector.split(" ")[1])
                total = int(total_pagination_selector.split(" ")[4])
            
            
            
            prev_count = len(home_card_list)
            await page.evaluate("window.scrollBy(0,(document.body.scrollHeight - 1600))")
            await page.wait_for_timeout(5000)
            
            
            data = await page.content()
            # import time
            # time.sleep(10)
            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'card card--default card--object card--object--properties')]")
            # await page.wait_for_selector("div.js-animate-fadein", timeout=6000)
            print(len(home_card_list))
            if (len(home_card_list) > prev_count):
                if total == currently_loaded:
                    return home_card_list
                else:
                    continue
            else:
                return home_card_list
    async def parse(self, response):
        try:
            page = response.meta["playwright_page"]
            # await page.evaluate(self.slow_scroll_js())
            
            
            data = await page.content() 
            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'card card--default card--object card--object--properties')]")
            home_card_list = await self.scroll(home_card_list, page, data)

            print(f"count of home list : {len(home_card_list)}")
            for home_card in home_card_list:
                url = self.allowed_domains[0] + home_card.xpath("./a").attrib['href']
                
                await page.wait_for_selector("//div[contains(@class, 'card card--default card--object card--object--properties')]//div[contains(@class, 'card-inner')]//div[contains(@class, 'card--default__figure__header')]//div[contains(@class,'card--object__slider')]/figure[1]/picture/picture")
                
                image_url = home_card.xpath(".//div[contains(@class, 'card card--default card--object card--object--properties')]//div[contains(@class, 'card-inner')]//div[contains(@class, 'card--default__figure__header')]//div[contains(@class,'card--object__slider')]/figure[1]/picture/picture").get()
            
            #     # image_url = re.search(r"background-image:\s*url\(&quot;(.*?)&quot;\);",image_url).group(1)
                city = ""
                city = home_card.xpath(".//div[contains(@class, 'card--default__content')]//div[contains(@class, 'card--default__body')]/small/text()").get()
                if city is None:
                    city = city.strip()
                address = ""
                address = home_card.xpath(".//div[contains(@class, 'card--default__content')]//div[contains(@class, 'card--default__body')]/h5/text()").get()
                if address is not None:
                    address = address.strip()
                    address = address + "," + city
                    
                city = city.split(",")
                if len(city) > 1:
                    city = city[1].strip()
                    city = parse_city_string(city)
                
                price = home_card.xpath(".//div[contains(@class, 'card--default__content')]//footer[contains(@class, 'card--default__footer')]/strong/text()").get()
                print(f"price : {price}")
                splitted_price = price.split(" ")
                if (len(splitted_price) > 0):
                    price = splitted_price[0]
                    price=  price[2:].strip()
                    price = price.replace('.', '')
                    
                agency = self.name
                room_count = home_card.xpath(".//footer[contains(@class, 'card--default__footer')]/ul/li[last()]/small/text()").get()
                if room_count is not None:
                    room_count = room_count.strip()
                    room_count = room_count.split(" ")[0]
                else:
                    room_count = "1"
                
                print(f"url : {url}")
                print(f"image_Url = {image_url}")
                print(f"city : {city}")
                print(f"address : {address}")
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
                yield HomeRentalInfoScraperItem(home=home)
        except Exception as e:
            print(f"Error while parsing: {e}")    
            traceback.print_exc()
