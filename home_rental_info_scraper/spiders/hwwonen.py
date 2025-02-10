import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class HwwonenSpider(SimilarWebScrapper):
    name = "hwwonen"
    allowed_domains = ["www.thuisbijhwwonen.nl"]
    start_urls = ["https://www.thuisbijhwwonen.nl/aanbod/nu-te-huur/huurwoningen"]
    
