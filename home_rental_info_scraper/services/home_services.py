from models.Home import Home
from config.db_handler import query_db
from utils import util

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
    home_value_str = util.convert_tuple_list_to_str(home_list)
    # there will be a problem since the parameter is a str, inserting price value might invoke exception need to work on that
    try:
        result = query_db("insert into homes(name, url, image_url) values %s)", params=[home_value_str])
        
        if result is not None:
            return True
        else:
            return False
        
    except Exception as e:
        print(e.__cause__)
        return False