from scrapy.crawler import CrawlerProcess,CrawlerRunner
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from home_rental_info_scraper.spiders import ooms,oostwestwonen,pararius
from home_rental_info_scraper.services.home_services import get_unique_home_list,save_new_homes,send_email_notification_on_user_preferences
import logging
from home_rental_info_scraper.models.Home import Home
import json
import jsonpickle
import traceback
import asyncio

def spider_results():
    try:
        results = []
        spider_list = [ooms.OomsSpider, oostwestwonen.OostwestwonenSpider, pararius.ParariusSpider]
        def crawler_results(signal, sender, item, response, spider):
            results.append(item)
            

        # dispatcher.connect(crawler_results, signal=signals.item_passed)

        process = CrawlerProcess(get_project_settings())
        for spider_item in spider_list:
            process.crawl(spider_item)
        
            for crawler in process.crawlers:
                crawler.signals.connect(crawler_results, signal = signals.item_passed)
            
        process.start()
            
            
        
        # process = CrawlerProcess(get_project_settings())
        # process.crawl(spider_list[0][0])
        # for crawler in process.crawlers:
        #     crawler.signals.connect(crawler_results, signal = signals.item_passed)
        # process.start()
        
        return results
    except Exception as e:
        print(f"Error in spider_results : {e}")
        traceback.print_exc()
        return None


def start_scraping():
    try:
        result = spider_results()
        if result is not None:
            print(result)
            print(f"Printing the count of result : {len(result)}")


            home_list = list()
            for item in result:
                home_list.append(item["home"])
                
            logging.info(f"checking the home list :{home_list[0].address}")
            unique_home_list = get_unique_home_list(home_list)
            logging.info(f"printing the size of unique home_list {len(unique_home_list)}")
            if len(unique_home_list) > 0:
                # saving the generated data 
                # data = json.dumps(unique_home_list)
                data = jsonpickle.encode(unique_home_list, unpicklable=False)
                with open("log2.json", "w") as f:
                    f.write(data)
                # ended
                send_email_notification_on_user_preferences(unique_home_list)
                if save_new_homes(unique_home_list=unique_home_list):
                    logging.info("New home list added to the database..")
                else:
                    logging.info("Something went wrong while trying to save home list to the database")
    except Exception as e:
        print(f"Exception happend while executing scraping operation.")
        import traceback; traceback.print_exc();


start_scraping()
