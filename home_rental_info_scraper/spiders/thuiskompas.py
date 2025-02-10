import scrapy


class ThuiskompasSpider(scrapy.Spider):
    name = "thuiskompas"
    allowed_domains = ["www.thuiskompas.nl"]
    start_urls = ["https://www.thuiskompas.nl/aanbod/nu-te-huur/te-huur/details/"]

    def parse(self, response):
        pass
