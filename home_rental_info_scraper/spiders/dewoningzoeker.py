import scrapy
from similar_web_scrapper import SimilarWebScrapper


class DewoningzoekerSpider(SimilarWebScrapper):
    name = "dewoningzoeker"
    allowed_domains = ["www.dewoningzoeker.nl"]
    start_urls = ["https://www.dewoningzoeker.nl/aanbod/te-huur#?gesorteerd-op=prijs%2B"]