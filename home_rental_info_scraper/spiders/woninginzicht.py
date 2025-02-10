import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class WoninginzichtSpider(SimilarWebScrapper):
    name = "woninginzicht"
    allowed_domains = ["www.woninginzicht.nl"]
    start_urls = ["https://www.woninginzicht.nl/aanbod/te-huur"]

    
