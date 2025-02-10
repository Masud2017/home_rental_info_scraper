import scrapy


class HollandrijnlandSpider(scrapy.Spider):
    name = "hollandrijnland"
    allowed_domains = ["www.hureninhollandrijnland.nl"]
    start_urls = ["https://www.hureninhollandrijnland.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
