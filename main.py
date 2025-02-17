from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from home_rental_info_scraper.spiders import vesteda,bouwinvest
import asyncio




async def spider_results():
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)
        

    dispatcher.connect(crawler_results, signal=signals.item_passed)

    process = CrawlerProcess(get_project_settings())
    process.crawl(bouwinvest.BouwinvestSpider)
    process.start()  # the script will block here until the crawling is finished
    return results

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

result = asyncio.run(spider_results())
print(f"printing the value of result {result}")

# todo
'''
At first need to check whether those home list are unique or not
After getting unique home send email notifications to the user based on their searchPreferences
Save unique homelist to the db
'''