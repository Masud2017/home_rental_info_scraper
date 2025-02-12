import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class FrieslandhuurtSpider(SimilarWebScrapper):
    name = "frieslandhuurt"
    allowed_domains = ["www.frieslandhuurt.nl"]
    start_urls = ["https://www.frieslandhuurt.nl/aanbod/nu-te-huur/huurwoningen"]