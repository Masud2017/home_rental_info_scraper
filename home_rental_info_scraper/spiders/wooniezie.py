import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class WooniezieSpider(SimilarWebScrapper):
    name = "wooniezie"
    allowed_domains = ["www.wooniezie.nl"]
    start_urls = ["https://www.wooniezie.nl/aanbod/nu-te-huur/te-huur"]

    
