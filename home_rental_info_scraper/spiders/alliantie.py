import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import json
import re
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.utils.util import parse_city_string
import time
import random
from home_rental_info_scraper.items import HomeRentalInfoScraperItem


def parse_alliantie(r:str):
    homes = []
    # jsonDataRegex = r'const\s+surveyJson\s*=\s*(\{.*?\});'
    # jsonDataRegex = r'Benopzoek\.properties\s*=\s*(\{.*?\});'
    jsonDataRegex = r'\s*Benopzoek\.properties\s*=\s*(\[\s?\{.*\}\]);'
    jsonData = re.search(jsonDataRegex, r, re.DOTALL).group(1)
    with open("log2.txt", "w",encoding='utf-8') as f:
        f.write(str(jsonData))
    
    results = json.loads(jsonData)["data"]
    
    for res in results:
        # Filter results not in selection because why the FUCK would you include
        # parameters and then not actually use them in your FUCKING API
        if not res["isInSelection"]:
            continue
            
        home = Home(agency="alliantie")
        home.address = res["address"]
        # this is a dirty hack because what website with rental homes does not
        # include the city AT ALL in their FUCKING API RESPONSES
        city_start = res["url"].index('/') + 1
        city_end = res["url"][city_start:].index('/') + city_start
        home.city = res["url"][city_start:city_end].capitalize()
        home.url = "https://ik-zoek.de-alliantie.nl/" + res["url"].replace(" ", "%20")
        home.price = int(res["price"][2:].replace('.', ''))
        homes.append(home)
        
        return homes

class AlliantieSpider(scrapy.Spider):
    name = "alliantie"
    allowed_domains = ["ik-zoek.de-alliantie.nl"]
    # start_urls = ["https://ik-zoek.de-alliantie.nl/aanbod?_gl=1*lkt4rw*_gcl_au*MTY5NjczODI4MC4xNzM5Mzg1NTc0*FPAU*MTY5NjczODI4MC4xNzM5Mzg1NTc0*_ga*NjE3NzA3NTQuMTczOTM4NTU3NQ..*_ga_479KG3CQM4*MTczOTUzMDY2NC4zLjAuMTczOTUzMDY3MS4wLjAuMzY3NDQ0Mzkz*_fplc*bTllR0o5WkZ2RnUxUXJwblNkamVwQ0pTSGszWU1MYXRqT21tMGl4Sm5mcE1udkV6d0ZsdHNsRkdZaXBDT0Q0R3B3STVhMHB5Y0VXaGFyUlNHQ0hJRUUlMkJXdGFZS1BNd1N5VHhhUG12T2VYcWpycFF3M2VmbzRPYWM1SzBKM3clM0QlM0Q."]
    start_urls = ["https://ik-zoek.de-alliantie.nl/huren/?page=1"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.result", timeout=6000),
                    PageMethod("click", "//div[contains(@class, 'cookie-bar__buttons')]/button/font/font"),
                    # PageMethod("wait_for_selector", ".filters.is-scrollable"),
                    # PageMethod("evaluate", self.slow_scroll_js()),

                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
            }
            
        )
    def scroll(self):
        return """
        async () => {
            const scrollableDiv = document.querySelector('.filters.is-scrollable');
            if (scrollableDiv) {
                scrollableDiv.scrollBy(0, scrollableDiv.scrollHeight);
            } else {
                console.error('Scrollable div not found!');
            }
        }
        """
        
        
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
                # instead doing the js thing in the start_requests, we can do it here
                await page.wait_for_selector(".filters.is-scrollable")
                await page.evaluate(self.slow_scroll_js())        
                # js = self.slow_scroll_js() is done
                data = await page.content()
                # home_card_list = Selector(text=data).xpath("//div[contains(@class, 'result')]")
                home_card_list = Selector(text=data).css("div.result")
                # with open("log.txt", "w", encoding="utf-8") as f:
                #     f.write(home_card_list.get())
                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    url = self.allowed_domains[0] + home_card.xpath("./a").attrib['href']
                    image_url = self.allowed_domains[0] + home_card.xpath(".//div[contains(@class, 'result__picture__slide slick-slide slick-current slick-active')]/img").attrib["src"]
                    city = ""
                    city = home_card.xpath(".//p[contains(@class, 'result__info__footer')]/span[1]/font/font/text()").get().strip()
                    room_count = home_card.xpath(".//p[contains(@class, 'result__info__footer')]/span[2]/font[2]/font/text()").get()
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[0]
                    address = ""
                    if city is not None:
                        address = home_card.xpath(".//div[contains(@class, 'result__info')]/h3/span/font/font/text()").get().strip() + "," + city
                        city = parse_city_string(city)
                    price = home_card.xpath(".//p[contains(@class, 'result__info__price')]/font/font/text()").get()
                    if price is not None:
                        price = price.split(" ")[0][1:]
                        # price = price.replace(".", "")
                        price = price.replace(",","")
                    else:
                        price = "0"
                    agency = self.name
                    
                    print(f"url : {url}")
                    print(f"image_Url = {image_url}")
                    print(f"address : {address}")
                    print(f"City : {city}")
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
                
                has_next = response.meta["playwright_page"].locator("//a[contains(@class, 'results__pagination__nav-next is-visible')]")
                # disabled_var = await has_next.get_attribute("disabled")
                
                if await has_next.is_visible():
                    await has_next.click(force = True)
                    await response.meta["playwright_page"].wait_for_selector("div.result")  # Wait for new cards
                
                else:
                    break

        except Exception as e:
            print(f"Error in parsing: {e}")