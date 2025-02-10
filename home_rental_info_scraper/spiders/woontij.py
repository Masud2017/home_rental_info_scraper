import scrapy


class WoontijSpider(scrapy.Spider):
    name = "woontij"
    allowed_domains = ["www.wonenindekop.nl"]
    start_urls = ["https://www.wonenindekop.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
