import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
import random
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
import re

class MakelaarshuisSpider(scrapy.Spider):
    name = "makelaarshuis"
    allowed_domains = ["yourexpatbroker.nl"]
    start_urls = ["https://yourexpatbroker.nl/woningaanbod?moveunavailablelistingstothebottom=true&orderby=3"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.object__holder", timeout=6000),
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    def slow_scroll_js(self):
        return f"""
        async () => {{
            const scrollableDiv = document.querySelector('.filters.is-scrollable');
            if (scrollableDiv) {{
                const totalHeight = scrollableDiv.scrollHeight;
                const step = totalHeight / 10; // Divide the scroll into 10 steps
                let currentPosition = 0;
                
                while (currentPosition < totalHeight) {{
                    currentPosition += step;
                    scrollableDiv.scrollBy(0, step);
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
            
            while True:
                data = await page.content()
                home_card_list = Selector(text=data).xpath("//div[contains(@class,  'object__holder')]")
                


                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    await page.evaluate(self.slow_scroll_js())
                    url = self.allowed_domains[0] + home_card.xpath(".//div[contains(@class,'object__data')]//a[contains(@class,'object__address-container')]").attrib['href']
                    # await page.wait_for_timeout(random.randint(4000, 7000))
                    
                    image_url = home_card.xpath(".//a[contains(@class,'swiper-slide swiper-slide-active')]/img").get()
                    image_url_regex = r'data-srcset="([^"]+)"'
                    print(f"Debugging the image url : {image_url}")
                    if(re.search(image_url_regex,image_url)):
                        image_url = re.search(image_url_regex,image_url).group(1)
                        image_url = image_url.strip()
                        image_url = image_url.split(",")[0]
                        image_url = image_url.split(" ")[0]
                        
                    # if image_url is not None:
                    #     image_url = image_url.split(",")[0]
                    #     image_url = image_url.split(" ")[0]
                    
                    city = home_card.xpath(".//div[contains(@class,'object__data')]//a[contains(@class , 'object__address-container')]//h3[contains(@class, 'object__address')]/span[2]/span[1]/text()").get().strip() + " "+ home_card.xpath(".//div[contains(@class,'object__data')]//a[contains(@class , 'object__address-container')]//h3[contains(@class, 'object__address')]/span[2]/span[2]/text()").get().strip()
                    
                    
                    if city is None:
                        city = ""
                    address = "" + city
                    address = home_card.xpath(".//div[contains(@class,'object__data')]//a[contains(@class , 'object__address-container')]//h3[contains(@class, 'object__address')]/span[1]/text()").get().strip() + "," + city
                    price = home_card.xpath(".//div[contains(@class,'object__data')]//a[contains(@class , 'object__address-container')]//h3[contains(@class, 'object__address')]/span[3]/text()").get().strip()
                    
                    room_count = home_card.xpath(".//span[contains(@class, 'object__features')]/span[2]/span/text()").get()
            
                    print(f"Debugging the price {price}")
                    
                    if price is not None:
                        price = price.split(",")[0]
                        price = price[2:]
                        
                    agency = self.name
                    
                    print("\n--------------------------")
                    print(f"url : {url}")
                    print(f"image_Url = {image_url}")
                    print(f"address : {address}")
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
                    
                has_next = response.meta["playwright_page"].locator("//li[contains(@class, 'page-item sys_paging next-page')]")
                    
                if await has_next.is_visible():
                    cls_next = await has_next.get_attribute("class")
                    print(f"debugging the next page : {cls_next}")
                    if cls_next == "page-item sys_paging next-page":
                        await has_next.click()
                        await response.meta["playwright_page"].wait_for_selector("div.projectproperty-tile")  # Wait for new cards
                else:
                    break
                    
        except Exception as e:
            print(f"Error while parsing : {e}")