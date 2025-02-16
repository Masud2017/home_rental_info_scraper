import scrapy


class ReboSpider(scrapy.Spider):
    name = "rebo"
    allowed_domains = ["www.rebogroep.nl"]
    start_urls = ["https://www.rebogroep.nl/nl/aanbod"]

    def parse(self, response):
        pass
