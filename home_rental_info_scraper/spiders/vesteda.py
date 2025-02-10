import scrapy


class VestedaSpider(scrapy.Spider):
    name = "vesteda"
    allowed_domains = ["www.vesteda.com"]
    start_urls = ["https://www.vesteda.com/nl/woning-zoeken?placeType=0&sortType=0&radius=20&s=&sc=woning&latitude=0&longitude=0&filters=0&priceFrom=500&priceTo=9999"]

    def parse(self, response):
        print(response.text)
