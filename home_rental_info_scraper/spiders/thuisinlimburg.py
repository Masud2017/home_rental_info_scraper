import scrapy


class ThuisinlimburgSpider(scrapy.Spider):
    name = "thuisinlimburg"
    allowed_domains = ["www.thuisinlimburg.nl"]
    start_urls = ["https://www.thuisinlimburg.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
