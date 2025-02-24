import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string

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
                const totalHeight = document.body.scrollHeight;
                const step = totalHeight / 10; // Divide the scroll into 10 steps
                let currentPosition = 0;
                
                while (currentPosition < totalHeight) {{
                    currentPosition += step;
                    window.scrollBy(0, step);
                    await new Promise(resolve => setTimeout(resolve, 200));
                }}
            }} else {{
                console.error('Scrollable element not found!');
            }}
        }}
        """
    async def parse(self, response):
        try:
            page = response.meta["playwright_page"]
            await page.evaluate(self.slow_scroll_js())
            
            data = await page.content()
            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'card card--default card--object card--object--properties')]")
            

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
