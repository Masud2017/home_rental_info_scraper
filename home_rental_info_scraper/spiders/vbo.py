import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.items import HomeRentalInfoScraperItem
from home_rental_info_scraper.utils.util import parse_city_string
import traceback

class VboSpider(scrapy.Spider):
    name = "vbo"
    allowed_domains = ["www.vbo.nl"]
    start_urls = ["https://www.vbo.nl/huurwoningen"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.col-lg-4", timeout=6000)
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
                home_card_list = Selector(text=data).xpath("//div[contains(@class, 'col-12 col-sm-6 col-lg-4')]")

                await page.wait_for_selector("//a[contains(@class, 'propertyLink')]", timeout=6000)

                print(f"count of home list : {len(home_card_list)}")
                for home_card in home_card_list:
                    url = home_card.xpath("./a").attrib['href']
                    image_url = home_card.xpath("./a/figure/img").attrib["src"]
                    # # with open("log.txt", "w", encoding = "utf-8") as f:
                    # #     f.write(image_url)
                    # # image_url = re.search(r"background-image:\s*url\(&quot;(.*?)&quot;\);",image_url).group(1)
                    # time.sleep(random.randint(3, 10))
                    city = home_card.xpath(".//a[contains(@class, 'propertyLink')]/figure/figcaption/span[2]/text()").get().strip()
                    # debugging purpose only
                    # print(f"debugging the value of city : {home_card.xpath("//a[contains(@class, 'propertyLink')]/figure/figcaption/span[1]").get()}")
                    
                    if city is None:
                        city = ""
                    address = "" + city
                    if city is not None:
                        address = home_card.xpath(".//a[contains(@class, 'propertyLink')]/figure/figcaption/span[1]/text()").get().strip() + "," + city
                        city = parse_city_string(city)
                    price = home_card.xpath(".//a[contains(@class, 'propertyLink')]/figure/figcaption/span[3]/text()").get()
                    if price is not None:
                        price = price.split(" ")[1]
                        price = price.split(",")[0]
                        price = price.replace(".", "")
                        price = price.replace(",", ".")
                    else:
                        price = "0"
                    agency = self.name
                    room_count = home_card.xpath("//div[contains(@class, 'bottom d-none d-md-block')]/ul/li[last()]/text()").get()
                    if room_count is not None:
                        room_count = room_count.strip()
                        room_count = room_count.split(" ")[-1]
                    
                    print("\n--------------------------")
                    print(f"url : {url}")
                    print(f"image_Url = {image_url}")
                    print(f"address : {address}")
                    print(f"city : {city}")
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
                    
                    
                    # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
                await page.wait_for_timeout(4000)    
                has_next = response.meta["playwright_page"].locator("//ul[contains(@class, 'pagination')]//li[last()]")
                
                if await has_next.is_visible():
                    cls_next = await has_next.get_attribute("class")
                    print(f"debugging the next page : {cls_next}")
                    if cls_next == "page-item":
                        await has_next.click()
                        await response.meta["playwright_page"].wait_for_selector("div.col-lg-4")  # Wait for new cards
                else:
                    break
                    

        except Exception as e:
            print(f"Error while parsing : {e}")
            traceback.print_exc()
