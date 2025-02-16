from models.Home import Home
from config.db_handler import query_db

def get_unique_home_list(home_list : Home)-> list[Home]:
    homes = query_db("select * from homes;")
    unique_home_list = list()
    
    if homes is not None:
        for home_item in home_list:
            if home_item in homes:
                continue
            else:
                unique_home_list.append(home_item)
                
                
        return unique_home_list
    
    
def save_new_homes(home_list:Home)-> bool:
    
    query_db("insert into homes(name, url, image_url) values()")
    return False