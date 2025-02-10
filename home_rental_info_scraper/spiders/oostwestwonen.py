import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class OostwestwonenSpider(SimilarWebScrapper):
    name = "oostwestwonen"
    allowed_domains = ["woningzoeken.oostwestwonen.nl"]
    start_urls = ["https://woningzoeken.oostwestwonen.nl/aanbod/nu-te-huur/huurwoningen"]

