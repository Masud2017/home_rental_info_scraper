import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class WoninghurenSpider(SimilarWebScrapper):
    name = "woninghuren"
    allowed_domains = ["www.woninghuren.nl"]
    start_urls = ["https://www.woninghuren.nl/aanbod/te-huur"]

