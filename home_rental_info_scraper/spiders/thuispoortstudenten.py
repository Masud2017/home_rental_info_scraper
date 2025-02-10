import scrapy


class ThuispoortstudentenSpider(scrapy.Spider):
    name = "thuispoortstudenten"
    allowed_domains = ["www.thuispoortstudentenwoningen.nl"]
    start_urls = ["https://www.thuispoortstudentenwoningen.nl/aanbod/details/"]

    def parse(self, response):
        pass
