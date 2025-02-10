import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class ThuiskompasSpider(SimilarWebScrapper):
    name = "thuiskompas"
    allowed_domains = ["www.thuiskompas.nl"]
    start_urls = ["https://www.thuiskompas.nl/aanbod/nu-te-huur/te-huur"]

