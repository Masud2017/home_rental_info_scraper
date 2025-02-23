from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from home_rental_info_scraper.spiders import vesteda,bouwinvest,woonzeker,woonnet_rijnmond,alliantie,funda,makelaarshuis,rebo,antares
from home_rental_info_scraper.services.home_services import get_unique_home_list,save_new_homes,send_email_notification_on_user_preferences



def spider_results():
    try:
        results = []

        def crawler_results(signal, sender, item, response, spider):
            results.append(item)
            

        # dispatcher.connect(crawler_results, signal=signals.item_passed)

        process = CrawlerProcess(get_project_settings())
        process.crawl(alliantie.AlliantieSpider)
        
        for crawler in process.crawlers:
            crawler.signals.connect(crawler_results, signal = signals.item_passed)
        
        process.start()  # the script will block here until the crawling is finished
        return results
    except Exception as e:
        print(f"Error in spider_results : {e}")
        return None


result = spider_results()
if result is not None:
    print(result)
    print(f"Printing the count of result : {len(result)}")


    home_list = list()
    for item in result:
        home_list.append(item["home"])
        
    print(f"checking the home list :{home_list[0].address}")
    unique_home_list = get_unique_home_list(home_list)
    print(f"printing the size of unique home_list {len(unique_home_list)}")
    if len(unique_home_list) > 0:
        # send_email_notification_on_user_preferences(unique_home_list)
        save_new_homes(unique_home_list=unique_home_list)