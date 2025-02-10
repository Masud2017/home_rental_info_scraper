import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class ThuisindeachterhoekSpider(SimilarWebScrapper):
    name = "thuisindeachterhoek"
    allowed_domains = ["www.thuisindeachterhoek.nl"]
    start_urls = ["https://www.thuisindeachterhoek.nl/aanbod/te-huur"]
