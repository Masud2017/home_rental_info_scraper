from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.config.db_handler import query_db
from home_rental_info_scraper.utils import util
from home_rental_info_scraper.config.email_handler import EmailHandler
from home_rental_info_scraper.services.whats_up_handler import WhatsAppHandler
import traceback
import datetime
import time
import os
from dotenv import load_dotenv


load_dotenv()

def exitsIn(scraped_home_item, old_home_list)-> bool:
    for old_home_item in old_home_list:
        if scraped_home_item.address == old_home_item["address"] and \
        util.parse_price_based_on_base(scraped_home_item.price) == util.parse_price_based_on_base(str(old_home_item["price"])) and \
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
    try:
        # result = query_db("insert into homes(address,city, url, agency,date_added, price, image_url,room_count) values %s", params=[str([x.get_home_tuple() for x in unique_home_list]).strip('[]')])
        query_st = "insert into homes(address,city, url, agency,date_added, price, image_url,room_count) values "
        place_holder = ",".join(['%s']*len(unique_home_list))
        query_st = query_st + place_holder
        result = query_db(query_st, params=[x.get_home_tuple() for x in unique_home_list])
        

        return True
        
    except Exception as e:
        print(f"Found error : {e}")
        traceback.print_exc()
        return False
    
def send_email_notification_on_user_preferences(unique_home_list:list[Home]):
    email_handler = EmailHandler()
    user_list = query_db("select * from users;")
    for user_item in user_list:
        if user_item["email"] is not None:
            search_pref = query_db("select * from search_preferences where user_id=%s", params=[str(user_item["id"])],fetchOne=True)
            if search_pref is not None:
                if search_pref["cities"] == None:
                    search_pref["cities"] = []
                sendable_home_list = list()
                for home_item in unique_home_list:
                    price = None
                    if home_item.price is not None:
                        if "." in home_item.price:
                            price = float(home_item.price)
                        elif home_item.price == '':
                            price = 0
                        else:
                            price = int(home_item.price)
                    else:
                        price = 0
                            
                    if home_item.city == None:
                        home_item.city = ""
                    
                    if (price >= int(search_pref["min_price"]) and
                        price <= int(search_pref["max_price"])) and\
                        home_item.city.casefold() in search_pref["cities"] and \
                        int(home_item.room_count) >= int(search_pref["min_rooms"]) and \
                        int(home_item.room_count) <= int(search_pref["max_rooms"]):
                            sendable_home_list.append(home_item)
                print(f"Size of sendable home list : {len(sendable_home_list)}")

                # filtering the sendable_home_list
                sendable_home_list = util.filter_sendable_home_list(sendable_home_list)
                # filtering section ended
                
                if len(sendable_home_list) > 0:
                    if len(sendable_home_list) > 8:
                        sendable_home_list_batch = util.divide_into_bactches(sendable_home_list=sendable_home_list)
                        for sendable_home_list_item in sendable_home_list_batch:
                            email_message = email_handler.generate_email_message(sendable_home_list_item)
                            ts = time.time()
                            email_handler.send_single_email(user_item["email"],f"PandjesPost - New home’s found", email_message,home_list=sendable_home_list_item, home_count= len(sendable_home_list_item))    
                    else:
                        email_message = email_handler.generate_email_message(sendable_home_list)
                        ts = time.time()
                        email_handler.send_single_email(user_item["email"],f"PandjesPost - New home’s found", email_message,home_list=sendable_home_list, home_count= len(sendable_home_list))
        
        
def send_whatsapp_notification_on_user_preferences(unique_home_list:list[Home]):
    whats_app_handler = WhatsAppHandler()
    user_list = query_db("select * from users;")
    for user_item in user_list:
        if user_item["email"] is not None:
            search_pref = query_db("select * from search_preferences where user_id=%s", params=[str(user_item["id"])],fetchOne=True)
            if search_pref is not None:
                if search_pref["cities"] == None:
                    search_pref["cities"] = []
                sendable_home_list = list()
                for home_item in unique_home_list:
                    price = None
                    if home_item.price is not None:
                        if "." in home_item.price:
                            price = float(home_item.price)
                        elif home_item.price == '':
                            price = 0
                        else:
                            price = int(home_item.price)
                    else:
                        price = 0
                            
                    if home_item.city == None:
                        home_item.city = ""
                    
                    if (price >= int(search_pref["min_price"]) and
                        price <= int(search_pref["max_price"])) and\
                        home_item.city.casefold() in search_pref["cities"] and \
                        int(home_item.room_count) >= int(search_pref["min_rooms"]) and \
                        int(home_item.room_count) <= int(search_pref["max_rooms"]):
                            sendable_home_list.append(home_item)
                print(f"Size of sendable home list : {len(sendable_home_list)}")

                # filtering the sendable_home_list
                sendable_home_list = util.filter_sendable_home_list(sendable_home_list)
                # filtering section ended
                
                if len(sendable_home_list) > 0:
                    if len(sendable_home_list) > 8:
                        sendable_home_list_batch = util.divide_into_bactches(sendable_home_list=sendable_home_list)
                        for sendable_home_list_item in sendable_home_list_batch:
                            whats_app_message = whats_app_handler.generate_message(sendable_home_list_item)
                            ts = time.time()
                            whats_app_handler.send_message(to=user_item["phone_number"], body= whats_app_message)    
                    else:
                        whats_app_message = whats_app_handler.generate_message(sendable_home_list)
                        ts = time.time()
                        whats_app_handler.send_single_email(to=user_item["phone_number"], body = email_message)