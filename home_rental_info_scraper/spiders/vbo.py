import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector

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
        page = response.meta["playwright_page"]
        
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
            address = home_card.xpath(".//a[contains(@class, 'propertyLink')]/figure/figcaption/span[1]/text()").get().strip() + "," + city
            price = home_card.xpath(".//a[contains(@class, 'propertyLink')]/figure/figcaption/span[3]/text()").get()
            price = price.split(" ")[1]
            price = price.split(",")[0]
            agency = self.name
            
            print("\n--------------------------")
            print(f"url : {url}")
            print(f"image_Url = {image_url}")
            print(f"address : {address}")
            print(f"price : {price}")
            print(f"Name : {agency}")
            print("--------------------------\n")
            
            
            # next_page = Selector(text = data).xpath("//div[contains(@class , 'results__pagination')]//a[contains(@class, 'results__pagination__nav-next')]").get()
            
        has_next = response.meta["playwright_page"].locator("//ul[contains(@class, 'pagination')]//li[last()]")
            
            
           
        if await has_next.is_visible():
            await has_next.click()
            await response.meta["playwright_page"].wait_for_selector("div.col-lg-4")  # Wait for new cards
            yield scrapy.Request(
                response.url,
                meta={"playwright": True, "playwright_include_page": True},
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                },
                callback=self.parse
            )
        else:
            print("All the pages finished scraping")
            
