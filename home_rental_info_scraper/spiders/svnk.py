import scrapy
from .similar_web_scrapper import SimilarWebScrapper


class SvnkSpider(SimilarWebScrapper):
    name = "svnk"
    allowed_domains = ["www.svnk.nl"]
    start_urls = ["https://www.svnk.nl/aanbod/nu-te-huur/huurwoningen"]

