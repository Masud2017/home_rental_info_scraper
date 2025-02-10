import scrapy


class MosaicPlazaSpider(scrapy.Spider):
    name = "mosaic-plaza"
    allowed_domains = ["plaza.newnewnew.space"]
    start_urls = ["https://plaza.newnewnew.space/aanbod/huurwoningen/details/"]

    def parse(self, response):
        pass
