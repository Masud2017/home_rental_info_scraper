import scrapy


class WooniezieSpider(scrapy.Spider):
    name = "wooniezie"
    allowed_domains = ["www.wooniezie.nl"]
    start_urls = ["https://www.wooniezie.nl/aanbod/nu-te-huur/te-huur/details/"]

    def parse(self, response):
        pass
