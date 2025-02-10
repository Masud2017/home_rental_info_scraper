import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class KlikvoorwonenSpider(SimilarWebScrapper):
    name = "klikvoorwonen"
    allowed_domains = ["www.klikvoorwonen.nl"]
    start_urls = ["https://www.klikvoorwonen.nl/aanbod/nu-te-huur/huurwoningen"]
    
