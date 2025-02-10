import scrapy


class ThuispoortSpider(scrapy.Spider):
    name = "thuispoort"
    allowed_domains = ["www.thuispoort.nl"]
    start_urls = ["https://www.thuispoort.nl/aanbod/te-huur/details/"]

    def parse(self, response):
        pass
