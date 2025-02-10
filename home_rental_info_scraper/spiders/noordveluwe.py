import scrapy


class NoordveluweSpider(scrapy.Spider):
    name = "noordveluwe"
    allowed_domains = ["www.hurennoordveluwe.nl"]
    start_urls = ["https://www.hurennoordveluwe.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
