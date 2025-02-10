import scrapy


class WoonkeusstedendriehoekSpider(scrapy.Spider):
    name = "woonkeusstedendriehoek"
    allowed_domains = ["www.woonkeus-stedendriehoek.nl"]
    start_urls = ["https://www.woonkeus-stedendriehoek.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
