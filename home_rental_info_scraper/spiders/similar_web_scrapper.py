import scrapy
import traceback
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
from ..items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string

class SimilarWebScrapper(scrapy.Spider):
    def start_requests(self):
        page_method_list = list()
        if self.name == "woninginzicht":
            page_method_list.append(PageMethod("click", "//button[contains(@id , 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')]"))
        page_method_list.append(PageMethod("wait_for_selector", "div.list-item-content", timeout=6000),)
        
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": page_method_list
                    
                    
                ,
                # "page_number": 1
            },
            # headers ={}
        )

    def slow_scroll_js(self):
        return f"""
        async () => {{
            const scrollableDiv = true
            if (scrollableDiv) {{
                var totalHeight = document.body.scrollHeight;
                const step = totalHeight / 10; // Divide the scroll into 10 steps
                let currentPosition = 0;
                
                while (currentPosition < totalHeight) {{
                    currentPosition += step;
                    window.scrollBy(0, step);
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

    async def parse(self, response):
        try:
            page = response.meta["playwright_page"]
            
            # auto scrolling mechanism
            await page.evaluate(self.slow_scroll_js())
            # auto scrolling mechanism ended
            
            
        
            data = await page.content()
            home_card_list = Selector(text=data).xpath("//div[contains(@class, 'list-item-content')]")
            print(len(home_card_list))
            for home_card in home_card_list:
                image_url = self.allowed_domains[0] + home_card.xpath(".//img/@src").get()
                # street = home_card.xpath(".//div[contains(@class, 'object-address')]/span[1]/span/text()").get()
                city = home_card.xpath(".//div[contains(@class, 'object-address')]//span[contains(@class, 'address-part')][2]/text()").get()
                address = ""

                if city is not None:
                    # print(f"city before parsing : {city}")
                    # city = parse_city_string(city)
                    if city is None:
                        city = ""
                    street = home_card.xpath(".//div[contains(@class, 'object-address')]/span[1]/span/text()").get()
                    
                    if street is not None:
                        print(f"street  : {street}")
                        print(f"city : {city}")
                        second_part = home_card.xpath(".//div[contains(@class, 'object-address')]/span[1]/text()").get()
                        if second_part is not None:
                            print(f"second part : {second_part}")
                            address = f"{street}{second_part}, {city}"
                
                agency = self.name
                price = home_card.xpath(".//span[contains(@class, 'kosten-regel2')]/text()").get()
                if price is not None:
                    price = price.split(" ")
                    if len(price) > 1:
                        price = price[2][2:]
                        # CONVERTING FROM EUROPEAN FORMAT TO AMERICAN FORMAT (CURRENCY)
                        if "." in price:
                            price = price.replace(".", "")
                        if "," in price:
                            price = price.replace(",", ".")
                        
                url = self.allowed_domains[0] + home_card.xpath(".//a[contains(@ng-click,'goToDetails')]").attrib['href']
                
                print(f"Image : {image_url}")
                print(f"Price : {price}")
                print(f"Address : {address}")
                print(f"URL : {url}")
                print(f"City : {city}")
                print(f"Agency : {agency}")            
                
                home = Home(
                    image_url=image_url,
                    address=address,
                    city=city,
                    agency=agency,
                    price=price,
                    url=url
                )
                yield HomeRentalInfoScraperItem(home=home)
        except Exception as e:
            print(f"Error : {e}")
            traceback.print_exc()