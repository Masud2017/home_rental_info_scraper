import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class WoonnethaaglandenSpider(SimilarWebScrapper):
    name = "woonnethaaglanden"
    allowed_domains = ["www.woonnet-haaglanden.nl"]
    start_urls = ["https://www.woonnet-haaglanden.nl/aanbod/nu-te-huur/te-huur"]

    
