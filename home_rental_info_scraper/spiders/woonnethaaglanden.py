import scrapy


class WoonnethaaglandenSpider(scrapy.Spider):
    name = "woonnethaaglanden"
    allowed_domains = ["www.woonnet-haaglanden.nl"]
    start_urls = ["https://www.woonnet-haaglanden.nl/aanbod/nu-te-huur/te-huur/details/"]

    def parse(self, response):
        pass
