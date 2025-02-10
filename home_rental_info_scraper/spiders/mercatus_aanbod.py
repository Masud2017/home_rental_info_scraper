import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class MercatusAanbodSpider(SimilarWebScrapper):
    name = "mercatus-aanbod"
    allowed_domains = ["woningaanbod.mercatus.nl"]
    start_urls = ["https://woningaanbod.mercatus.nl/aanbod/te-huur"]
    
