import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import json
import re
from home_rental_info_scraper.models.Home import Home
import time


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
    start_urls = ["https://ik-zoek.de-alliantie.nl/aanbod?_gl=1*lkt4rw*_gcl_au*MTY5NjczODI4MC4xNzM5Mzg1NTc0*FPAU*MTY5NjczODI4MC4xNzM5Mzg1NTc0*_ga*NjE3NzA3NTQuMTczOTM4NTU3NQ..*_ga_479KG3CQM4*MTczOTUzMDY2NC4zLjAuMTczOTUzMDY3MS4wLjAuMzY3NDQ0Mzkz*_fplc*bTllR0o5WkZ2RnUxUXJwblNkamVwQ0pTSGszWU1MYXRqT21tMGl4Sm5mcE1udkV6d0ZsdHNsRkdZaXBDT0Q0R3B3STVhMHB5Y0VXaGFyUlNHQ0hJRUUlMkJXdGFZS1BNd1N5VHhhUG12T2VYcWpycFF3M2VmbzRPYWM1SzBKM3clM0QlM0Q."]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.result.is-loaded", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'result is-loaded')]")
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write(home_card_list.get())
        print(f"count of home list : {len(home_card_list)}")
        for home_card in home_card_list:
            url = self.allowed_domains[0] + home_card.xpath("./a").attrib['href']
            image_url = self.allowed_domains[0] + home_card.xpath(".//div[contains(@class, 'result__picture__slide slick-slide slick-current slick-active')]/img").attrib["src"]
            # city = ""
            # city = home_card.xpath(".//p[contains(@class, 'result__info__footer')]/span[1]/text()").get()
            # address = ""
            # address = home_card.xpath(".//div[contains(@class , 'result__info')]/h3/span/text()").get() + "," + city
            price = home_card.xpath(".//div[contains(@class, 'result__info__pricing')]//p[contains(@class, 'result__info__price')]/text()").get()
            
            print(f"url : {url}")
            print(f"image_Url = {image_url}")
            # print(f"address : {address}")
            print(f"price : {price}")
        




# home_card_list = Selector(text=data).xpath("//div[contains(@class, 'js-animate-fadein')]")
        
#         # with open("log.txt", "a") as f:
#         #         f.write(''.join(home_card_list.getall()))
#         print(f"Total Home Cards : {len(home_card_list)}")
#         for home_card in home_card_list:
#             url = self.allowed_domains[0] + home_card.xpath(".//a").attrib['href']
#             # await page.wait_for_selector("div['data-size-desktop']", timeout=6000)
            
            

#             image_url = home_card.xpath(".//div[contains(@class, 'swipe__list')]//div[contains(@class, 'swipe__item')][1]//div[contains(@class, 'swipe__image')]").get()
#             regex = r"background-image:url\(['\"]?(.*?)['\"]?\)"
#             image_url = re.search(regex, image_url).group(1)
#             if (len(image_url) > 2):
#                 image_url = image_url[2:]
                
#             city = home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box__properties')]//div[contains(@class, 'box__title')][2]/span/text()").get()
#             address = (home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box__properties')]//div[contains(@class, 'box__title')][1]/text()").get() + ","+ city).strip()
#             price = home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box--obj__price')]/text()").get()
#             agency = self.name
#             # date_added = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-card--listview-price')]/text()").get()
            
#             print(url)
#             print(f"image url : {image_url}")
#             print(f"city : {city}")
#             print(f"address: {address}")
#             print(f"price : {price}")
#             print(f"agency : {agency}")
            
