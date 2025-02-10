import scrapy


class ThuisindeachterhoekSpider(scrapy.Spider):
    name = "thuisindeachterhoek"
    allowed_domains = ["www.thuisindeachterhoek.nl"]
    start_urls = ["https://www.thuisindeachterhoek.nl/aanbod/te-huur/details/"]

    def parse(self, response):
        pass
