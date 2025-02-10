import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class ThuispoortstudentenSpider(SimilarWebScrapper):
    name = "thuispoortstudenten"
    allowed_domains = ["www.thuispoortstudentenwoningen.nl"]
    start_urls = ["https://www.thuispoortstudentenwoningen.nl/aanbod"]

