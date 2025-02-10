import scrapy


class ZuidwestwonenSpider(scrapy.Spider):
    name = "zuidwestwonen"
    allowed_domains = ["www.zuidwestwonen.nl"]
    start_urls = ["https://www.zuidwestwonen.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
