import scrapy


class OostwestwonenSpider(scrapy.Spider):
    name = "oostwestwonen"
    allowed_domains = ["woningzoeken.oostwestwonen.nl"]
    start_urls = ["https://woningzoeken.oostwestwonen.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
