import scrapy
from .similar_web_scrapper import SimilarWebScrapper

class AntaresSpider(SimilarWebScrapper):
    name = "antares"
    allowed_domains = ["wonen.thuisbijantares.nl"]
    start_urls = ["https://wonen.thuisbijantares.nl/aanbod/nu-te-huur/te-huur"]