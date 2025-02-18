def get_home_persistance_query(tuple_list:list[tuple]):
    string = "insert into homes(address,city, url, agency,date_added, price, image_url) values"
    for idx in range(0, len(tuple_list)):
        value_data = f"({tuple_list[idx].__str__()})"
        if idx >= len(tuple_list)-1:
            string = string + value_data + ";"
            break
        else:
            string = string + value_data + ","
        
    return string