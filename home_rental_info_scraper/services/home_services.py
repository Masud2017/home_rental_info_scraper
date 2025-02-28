from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.config.db_handler import query_db
from home_rental_info_scraper.utils import util
from home_rental_info_scraper.config.email_handler import EmailHandler
import traceback

def exitsIn(scraped_home_item, old_home_list)-> bool:
    for old_home_item in old_home_list:
        if scraped_home_item.address == old_home_item["address"] and \
        int(scraped_home_item.price) == int(old_home_item["price"]) and \
        scraped_home_item.city  == old_home_item["city"] and \
        scraped_home_item.url == old_home_item["url"] and \
        scraped_home_item.agency == old_home_item["agency"] and \
        scraped_home_item.image_url == old_home_item["image_url"] and \
        int(scraped_home_item.room_count) == int(old_home_item["room_count"]):
            return True
            
            
    return False
def get_unique_home_list(scraped_home_list : Home)-> list[Home]:
    old_home_list = query_db("select * from homes;")
    unique_home_list = list()
    
    if old_home_list is not None:
        for scraped_home_item in scraped_home_list:
            if exitsIn(scraped_home_item=scraped_home_item, old_home_list = old_home_list):
                continue
            else:
                unique_home_list.append(scraped_home_item)
                
    return unique_home_list



    
def save_new_homes(unique_home_list: Home) -> bool:
    # home_value_str = util.convert_tuple_list_to_str(unique_home_list)
    
    # there will be a problem since the parameter is a str, inserting price value might invoke exception need to work on that
    try:
        # result = query_db("insert into homes(name, url, image_url) values %s)", params=[home_value_str])
        # result = query_db(util.get_home_persistance_query(unique_home_list))
        result = query_db("insert into homes(address,city, url, agency,date_added, price, image_url,room_count) values "+str([x.get_home_tuple() for x in unique_home_list]).strip('[]'))
        print(f"Debugging the result : {result}")
        
        if result is not None:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Found error : {e}")
        traceback.print_exc()
        return False
    
def send_email_notification_on_user_preferences(unique_home_list:list[Home]):
    email_handler = EmailHandler()
    user_list = query_db("select * from users;")
    for user_item in user_list:
        if user_item["email"] == "msmasud578@gmail.com":
            search_pref = query_db("select * from search_preferences where user_id=%s", params=[str(user_item["id"])],fetchOne=True)
            if search_pref is not None:
                if search_pref["cities"] == None:
                    search_pref["cities"] = []
                sendable_home_list = list()
                for home_item in unique_home_list:
                    if (int(home_item.price) >= int(search_pref["min_price"]) and
                        int(home_item.price) <= int(search_pref["max_price"])) and\
                        home_item.city == search_pref["cities"] and \
                        int(home_item.room_count) >= int(search_pref["min_rooms"]) and \
                        int(home_item.room_count) <= int(search_pref["max_rooms"]):
                        sendable_home_list.append(home_item)
                print(f"Size of sendable home list : {sendable_home_list}")
                if len(sendable_home_list) > 0:
                    email_message = email_handler.generate_email_message(sendable_home_list)
                    email_handler.send_single_email(user_item["email"],"Home list notification", email_message)
        