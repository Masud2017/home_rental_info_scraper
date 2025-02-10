import scrapy


class WoninghurenSpider(scrapy.Spider):
    name = "woninghuren"
    allowed_domains = ["www.woninghuren.nl"]
    start_urls = ["https://www.woninghuren.nl/aanbod/te-huur/details/"]

    def parse(self, response):
        pass
