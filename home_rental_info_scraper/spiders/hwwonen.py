import scrapy


class HwwonenSpider(scrapy.Spider):
    name = "hwwonen"
    allowed_domains = ["www.thuisbijhwwonen.nl"]
    start_urls = ["https://www.thuisbijhwwonen.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
