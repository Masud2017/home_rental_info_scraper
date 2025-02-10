import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class NoordveluweSpider(SimilarWebScrapper):
    name = "noordveluwe"
    allowed_domains = ["www.hurennoordveluwe.nl"]
    start_urls = ["https://www.hurennoordveluwe.nl/aanbod/nu-te-huur/huurwoningen"]