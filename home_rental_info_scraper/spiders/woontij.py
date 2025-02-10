import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class WoontijSpider(SimilarWebScrapper):
    name = "woontij"
    allowed_domains = ["www.wonenindekop.nl"]
    start_urls = ["https://www.wonenindekop.nl/aanbod/nu-te-huur/huurwoningen"]

