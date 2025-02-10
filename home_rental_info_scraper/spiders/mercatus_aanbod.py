import scrapy


class MercatusAanbodSpider(scrapy.Spider):
    name = "mercatus-aanbod"
    allowed_domains = ["woningaanbod.mercatus.nl"]
    start_urls = ["https://woningaanbod.mercatus.nl/aanbod/te-huur/details/"]

    def parse(self, response):
        pass
