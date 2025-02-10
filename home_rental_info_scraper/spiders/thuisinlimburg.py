import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class ThuisinlimburgSpider(SimilarWebScrapper):
    name = "thuisinlimburg"
    allowed_domains = ["www.thuisinlimburg.nl"]
    start_urls = ["https://www.thuisinlimburg.nl/aanbod/nu-te-huur/huurwoningen"]

