import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

class IkwilhurenSpider(scrapy.Spider):
    name = "ikwilhuren"
    allowed_domains = ["ikwilhuren.nu"]
    start_urls = ["https://ikwilhuren.nu"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.card", timeout=6000)
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        data = await page.content()
        home_card_list = Selector(text=data).xpath("//div[contains(@class, 'card card-woning shadow-sm rounded-5 rounded-end-0 rounded-bottom-0 overflow-hidden flex-grow-1')]")
        print(f"Total Home Cards : {len(home_card_list)}")
        for home_card in home_card_list:
            url = self.allowed_domains[0] + home_card.xpath(".//a[contains(@class, 'stretched-link')]").attrib['href']

            image_url = home_card.xpath(".//div[contains(@class, 'card-img-top')]/div[2]/picture/img").attrib['src']
            if len(image_url) > 2:
                image_url = self.allowed_domains[0]+ image_url[17:]
            city = (home_card.xpath(".//div[contains(@class, 'card-body d-flex flex-column')]//span[contains(@class , 'card-title h5 text-secondary mb-0')]/following-sibling::span[1]/text()").get()).strip()
            address = (home_card.xpath(".//a[contains(@class, 'stretched-link')]/text()").get()).strip() + "," + city
            price = home_card.xpath(".//div[contains(@class, 'card-body d-flex flex-column')]/div/span[1]/text()").get()
            agency = self.name
            # date_added = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-card--listview-price')]/text()").get()
            
            print(f"url {url}")
            print(f"image url : {image_url}")
            print(f"city : {city}")
            print(f"address: {address}")
            print(f"price : {price}")
            print(f"agency : {agency}")
            
