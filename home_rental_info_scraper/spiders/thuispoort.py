import scrapy
from .similar_web_scrapper import SimilarWebScrapper



class ThuispoortSpider(SimilarWebScrapper):
    name = "thuispoort"
    allowed_domains = ["www.thuispoort.nl"]
    start_urls = ["https://www.thuispoort.nl/aanbod/te-huur"]

