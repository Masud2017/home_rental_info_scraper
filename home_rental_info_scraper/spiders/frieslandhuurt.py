import scrapy


class FrieslandhuurtSpider(scrapy.Spider):
    name = "frieslandhuurt"
    allowed_domains = ["www.frieslandhuurt.nl"]
    start_urls = ["https://www.frieslandhuurt.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
