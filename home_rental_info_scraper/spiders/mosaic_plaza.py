import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class MosaicPlazaSpider(SimilarWebScrapper):
    name = "mosaic-plaza"
    allowed_domains = ["plaza.newnewnew.space"]
    start_urls = ["https://plaza.newnewnew.space/aanbod/huurwoningen"]
