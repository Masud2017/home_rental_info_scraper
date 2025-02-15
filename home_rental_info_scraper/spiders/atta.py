import scrapy


class AttaSpider(scrapy.Spider):
    name = "atta"
    allowed_domains = ["atta.nl"]
    start_urls = ["https://atta.nl/woningaanbod/huuraanbod/"]

    def parse(self, response):
        pass
