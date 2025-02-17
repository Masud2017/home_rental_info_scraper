from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from home_rental_info_scraper.spiders import vesteda
import asyncio




def spider_results():
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(vesteda.VestedaSpider)
    process.start()  # the script will block here until the crawling is finished
    return results

result = spider_results()
print(f"printing the value of result {result}")