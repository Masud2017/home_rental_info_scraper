from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings
from home_rental_info_scraper.spiders import vesteda,bouwinvest,woonzeker,woonnet_rijnmond,alliantie
from home_rental_info_scraper.services.home_services import get_unique_home_list,save_new_homes,send_email_notification_on_user_preferences


def spider_results():
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
result = spider_results()
print(result)
print(f"Printing the count of result : {len(result)}")
# scraped_home_list = spider_results()
# todo
'''
At first need to check whether those home list are unique or not
After getting unique home send email notifications to the user based on their searchPreferences
Save unique homelist to the db
'''

from home_rental_info_scraper.models.Home import Home
# Create two dummy Home objects
  
home1 = Home(address="123 Main St", city="Springfield", url="http://example.com/123-main-st", agency="Agency1", price=1000, image_url="http://example.com/images/123-main-st.jpg")
home2 = Home(address="456 Elm St", city="Shelbyville", url="http://example.com/456-elm-st", agency="Agency2", price=1200, image_url="http://example.com/images/456-elm-st.jpg")
home3 = Home(address="789 Oak St", city="Capital City", url="http://example.com/789-oak-st", agency="Agency3", price=1300, image_url="http://example.com/images/789-oak-st.jpg")
home4 = Home(address="101 Pine St", city="Ogdenville", url="http://example.com/101-pine-st", agency="Agency4", price=1400, image_url="http://example.com/images/101-pine-st.jpg")
home5 = Home(address="202 Maple St", city="North Haverbrook", url="http://example.com/202-maple-st", agency="Agency5", price=1500, image_url="http://example.com/images/202-maple-st.jpg")
home6 = Home(address="303 Birch St", city="Brockway", url="http://example.com/303-birch-st", agency="Agency6", price=1600, image_url="http://example.com/images/303-birch-st.jpg")
home7 = Home(address="404 Cedar St", city="Springfield", url="http://example.com/404-cedar-st", agency="Agency7", price=1700, image_url="http://example.com/images/404-cedar-st.jpg")
home8 = Home(address="505 Walnut St", city="Shelbyville", url="http://example.com/505-walnut-st", agency="Agency8", price=1800, image_url="http://example.com/images/505-walnut-st.jpg")
home9 = Home(address="606 Pine St", city="Capital City", url="http://example.com/606-pine-st", agency="Agency9", price=1900, image_url="http://example.com/images/606-pine-st.jpg")
home10 = Home(address="707 Maple St", city="Ogdenville", url="http://example.com/707-maple-st", agency="Agency10", price=2000, image_url="http://example.com/images/707-maple-st.jpg")
home11 = Home(address="808 Birch St", city="North Haverbrook", url="http://example.com/808-birch-st", agency="Agency11", price=2100, image_url="http://example.com/images/808-birch-st.jpg")
scraped_home_list = [home1, home2, home3, home4, home5, home6, home7, home8, home9, home10, home11]
# home_list is basically the scraped data

# this needs to be used in future stuff 
home_list = list()
for item in result:
    home_list.append(item["home"])
    
print(f"checking the home list :{home_list[0].address}")
unique_home_list = get_unique_home_list(home_list)
print(f"printing the size of unique home_list {len(unique_home_list)}")
if len(unique_home_list) > 0:
    send_email_notification_on_user_preferences(unique_home_list)
    # save_new_homes(unique_home_list=unique_home_list)