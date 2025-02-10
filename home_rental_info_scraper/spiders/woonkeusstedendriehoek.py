import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class WoonkeusstedendriehoekSpider(SimilarWebScrapper):
    name = "woonkeusstedendriehoek"
    allowed_domains = ["www.woonkeus-stedendriehoek.nl"]
    start_urls = ["https://www.woonkeus-stedendriehoek.nl/aanbod/nu-te-huur/huurwoningen"]

    
