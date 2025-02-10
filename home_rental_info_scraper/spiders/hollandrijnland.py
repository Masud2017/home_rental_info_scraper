import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class HollandrijnlandSpider(SimilarWebScrapper):
    name = "hollandrijnland"
    allowed_domains = ["www.hureninhollandrijnland.nl"]
    start_urls = ["https://www.hureninhollandrijnland.nl/aanbod/nu-te-huur/huurwoningen"]
        
