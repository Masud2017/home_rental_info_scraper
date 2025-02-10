import scrapy


class KlikvoorwonenSpider(scrapy.Spider):
    name = "klikvoorwonen"
    allowed_domains = ["www.klikvoorwonen.nl"]
    start_urls = ["https://www.klikvoorwonen.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
