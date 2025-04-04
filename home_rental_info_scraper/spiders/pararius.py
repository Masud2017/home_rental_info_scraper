import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import re
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string


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
                    await new Promise(resolve => setTimeout(resolve, 800));
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
            data = await page.content()
            page_count = int(Selector(text = data).xpath("//ul[contains(@class, 'pagination__list')]//li[contains(@class , 'pagination__item pagination__item--spacer')]/following-sibling::li[1]/a/text()").get().strip())
            print(f"Printing the page count {page_count}")
            page_counter = 1
            
        
            while True:
                await page.evaluate(self.slow_scroll_js())
                data = await page.content()
                home_card_list = Selector(text=data).xpath("//li[contains(@class , 'search-list__item search-list__item--listing')]")

                # await page.wait_for_selector("//a[contains(@class, 'propertyLink')]", timeout=6000)

                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    url_portion = home_card.xpath(".//div[contains(@class,  'listing-search-item__depiction')]/a").attrib['href']
                    if url_portion is not None:
                        url = self.allowed_domains[0] + url_portion
                    else:
                        url = self.allowed_domains[0]
                    image_url = home_card.xpath(".//div[contains(@class,  'listing-search-item__depiction')]/a/wc-picture/picture//img[contains(@class, 'picture__image')]").get()
                    print(f"Debugging the image url : {image_url}")
                    if image_url is not None:
                        reg = r'src="([^"]+)"'
                        reg_alternative = r""
                        search = re.search(reg, image_url)
                        if search:
                            image_url = search.group(1)
                    
                    city = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//div[contains(@class ,'listing-search-item__sub-title')]/text()").get().strip()
                    
                    
                    if city is None:
                        city = ""
                    if city is not None:
                        city = parse_city_string(city)
                        city = city.replace('(','').replace(')','')
                    address = ""
                    address = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//h2[contains(@class,'listing-search-item__title')]/a/text()").get().strip()
                    if address is not None:
                        address = address + "," + city
                        address = address.replace('(','').replace(')','')
                    price = home_card.xpath(".//div[contains(@class,  'listing-search-item__content')]//div[contains(@class ,'listing-search-item__price')]/text()").get().strip()
                    print(f"Debugging the price {price}")
                    if price is not None:
                        price = price.split(" ")[0]
                        if len(price) > 0:
                            print(f"Yoyuo")
                            price = price.strip()
                            price = price[2:]
                            price = price.replace(".", "")
                    else:
                        price = "0"
                    agency = self.name
                    room_count = home_card.xpath(".//ul[contains(@class, 'illustrated-features illustrated-features--compact')]/li[2]/text()").get()
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[0]
                    else:
                        room_count = "1"
                    
                    print("\n--------------------------")
                    print(f"url : {url}")
                    print(f"image_Url = {image_url}")
                    print(f"address : {address}")
                    print(f"city : {city}")
                    print(f"price : {price}")
                    print(f"Name : {agency}")
                    print(f"Room count : {room_count}")
                    print("--------------------------\n")
                    if "ijs" not in price:
                        
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
                        
                
                if page_count > 5:
                    if page_counter == 5:
                        break
                page_counter = page_counter + 1
                    
                has_next = response.meta["playwright_page"].locator("//a[contains(@class, 'pagination__link pagination__link--next')]")
                print(f"debugging the next page : {has_next}")
                    
                if await has_next.is_visible():
                    # cls_next = await has_next.get_attribute("class")
                    # print(f"debugging the next page : {cls_next}")
                    # if cls_next == "active active-exact pagination__arrow pagination__next icon-caret-right":
                    await has_next.click()
                    await response.meta["playwright_page"].wait_for_selector("li.search-list__item")  # Wait for new cards
                else:
                    break
                
        except Exception as e:
            print(f"Error while parsing: {e}")
