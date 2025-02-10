import scrapy


class WoninginzichtSpider(scrapy.Spider):
    name = "woninginzicht"
    allowed_domains = ["www.woninginzicht.nl"]
    start_urls = ["https://www.woninginzicht.nl/aanbod/te-huur/details/"]

    def parse(self, response):
        pass
