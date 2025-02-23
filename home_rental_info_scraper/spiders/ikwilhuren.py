import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem

class IkwilhurenSpider(scrapy.Spider):
    name = "ikwilhuren"
    allowed_domains = ["ikwilhuren.nu"]
    start_urls = ["https://ikwilhuren.nu/aanbod/"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.card", timeout=6000),
                    PageMethod("click", "button.cc_button_allowall")
                ],
            },
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            
        )

    async def parse(self, response):
        try:
            page = response.meta["playwright_page"]
            
            while True:
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
                    if price is not None:
                        price = price.split(",")[0]
                        price = price[2:]
                        price = price.replace(".", "")
                    agency = self.name
                    room_count = home_card.xpath("//div[contains(@class, 'card-body d-flex flex-column')]/div/span[3]/text()").get()
                    
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[0]
                    # date_added = home_card.xpath(".//div[contains(@class, 'o-card--listview-content')]//div[contains(@class, 'o-card--listview-price')]/text()").get()
                    
                    print(f"url {url}")
                    print(f"image url : {image_url}")
                    print(f"city : {city}")
                    print(f"address: {address}")
                    print(f"price : {price}")
                    print(f"agency : {agency}")
                    print(f"room_count : {room_count}")
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
                
                
                has_next = response.meta["playwright_page"].locator("//div[contains(@class, 'd-flex flex-wrap gap-2')]/a[2]")
                    
                if await has_next.is_visible():
                    cls_next = await has_next.get_attribute("class")
                    print(f"debugging the next page : {cls_next}")
                    if cls_next == "btn btn-primary":
                        await has_next.click()
                        # await response.meta["playwright_page"].wait_for_selector("div.projectproperty-tile")  # Wait for new cards
                else:
                    break
        except Exception as e:
            print(f"Error while parsing : {e}")