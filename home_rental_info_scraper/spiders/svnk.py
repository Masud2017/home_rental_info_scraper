import scrapy


class SvnkSpider(scrapy.Spider):
    name = "svnk"
    allowed_domains = ["www.svnk.nl"]
    start_urls = ["https://www.svnk.nl/aanbod/nu-te-huur/huurwoningen/details/"]

    def parse(self, response):
        pass
