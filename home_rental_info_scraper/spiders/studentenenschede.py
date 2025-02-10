import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class StudentenenschedeSpider(SimilarWebScrapper):
    name = "studentenenschede"
    allowed_domains = ["www.roomspot.nl"]
    start_urls = ["https://www.roomspot.nl/aanbod/te-huur"]
