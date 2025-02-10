import scrapy


class StudentenenschedeSpider(scrapy.Spider):
    name = "studentenenschede"
    allowed_domains = ["www.roomspot.nl"]
    start_urls = ["https://www.roomspot.nl/aanbod/te-huur/details/"]

    def parse(self, response):
        pass
