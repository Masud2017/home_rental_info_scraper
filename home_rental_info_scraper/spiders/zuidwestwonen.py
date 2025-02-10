import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class ZuidwestwonenSpider(SimilarWebScrapper):
    name = "zuidwestwonen"
    allowed_domains = ["www.zuidwestwonen.nl"]
    start_urls = ["https://www.zuidwestwonen.nl/aanbod/nu-te-huur/huurwoningen"]
