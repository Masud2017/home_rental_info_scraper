import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

class AlliantieSpider(scrapy.Spider):
    name = "alliantie"
    allowed_domains = ["ik-zoek.de-alliantie.nl"]
    start_urls = ["https://ik-zoek.de-alliantie.nl/"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.js-animate-fadein", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'js-animate-fadein')]")
        
        # with open("log.txt", "a") as f:
        #         f.write(''.join(home_card_list.getall()))
        print(f"Total Home Cards : {len(home_card_list)}")
        for home_card in home_card_list:
            url = self.allowed_domains[0] + home_card.xpath(".//a").attrib['href']
            # await page.wait_for_selector("div['data-size-desktop']", timeout=6000)
            
            

            image_url = home_card.xpath(".//div[contains(@class, 'swipe__list')]//div[contains(@class, 'swipe__item')][1]//div[contains(@class, 'swipe__image')]").get()
            regex = r"background-image:url\(['\"]?(.*?)['\"]?\)"
            image_url = re.search(regex, image_url).group(1)
            if (len(image_url) > 2):
                image_url = image_url[2:]
                
            city = home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box__properties')]//div[contains(@class, 'box__title')][2]/span/text()").get()
            address = (home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box__properties')]//div[contains(@class, 'box__title')][1]/text()").get() + ","+ city).strip()
            price = home_card.xpath(".//a[contains(@class, 'clean')]//div[contains(@class, 'box--obj__price')]/text()").get()
            agency = self.name
            # date_added = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-card--listview-price')]/text()").get()
            
            print(url)
            print(f"image url : {image_url}")
            print(f"city : {city}")
            print(f"address: {address}")
            print(f"price : {price}")
            print(f"agency : {agency}")
            
