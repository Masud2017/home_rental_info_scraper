from home_rental_info_scraper.models.Home import Home

def get_home_persistance_query(tuple_list:list[tuple]):
    string = "insert into homes(address,city, url, agency,date_added, price, image_url,room_count) values"
    for idx in range(0, len(tuple_list)):
        value_data = f"({tuple_list[idx].__str__()})"
        if idx >= len(tuple_list)-1:
            string = string + value_data + ";"
            break
        else:
            string = string + value_data + ","
        
    return string


def parse_city_string(city_string: str) -> str:
    cities_netherlands = [
        # North Holland (Noord-Holland)
        "Amsterdam", "Haarlem", "Alkmaar", "Zaandam", "Hilversum", "Hoorn",
        # South Holland (Zuid-Holland)
        "Rotterdam", "The Hague", "Leiden", "Delft", "Dordrecht", "Gouda", "Zoetermeer",
        # Utrecht
        "Utrecht", "Amersfoort", "Veenendaal",
        # North Brabant (Noord-Brabant)
        "Eindhoven", "Tilburg", "Breda", "Den Bosch", "Helmond",
        # Gelderland
        "Arnhem", "Nijmegen", "Apeldoorn", "Ede",
        # Overijssel
        "Enschede", "Zwolle", "Deventer",
        # Limburg
        "Maastricht", "Venlo", "Heerlen",
        # Friesland (Fryslân)
        "Leeuwarden", "Sneek", "Drachten",
        # Groningen
        "Groningen",
        # Drenthe
        "Assen", "Emmen", "Meppel",
        # Flevoland
        "Almere", "Lelystad",
        # Zeeland
        "Middelburg", "Vlissingen", "Goes",
        "Heinkenszand"
    ]
    
    for city in cities_netherlands:
        # print(f"Printing the city : {city}")
        if city.lower() in city_string.lower():
            return city

    return city_string.split(" ")[-1]


def filter_sendable_home_list(sendable_home_list:list) -> list | None:
    filtered_home_list = []
    
    
    for home_item in sendable_home_list:
        if home_item.price is None:
            home_item.price = 0
        if home_item.city is None:
            home_item.city = ""
        if home_item.address is None:
            home_item.address = ""
        if home_item.url is None:
            home_item.url = ""
        if home_item.image_url is None:
            home_item.image_url = ""
        if home_item.agency is None:
            home_item.agency = ""
        if home_item.room_count is None:
            home_item.room_count = 0
            
        if len(home_item.city) > 0 and \
            len(home_item.address) > 0 and \
            len(home_item.price) > 0 and \
            len(home_item.url) > 0 and\
            len(home_item.image_url) > 0 and \
            len(home_item.agency) > 0 and\
            len(home_item.room_count) > 0:
            filtered_home_list.append(home_item)
            
    return filtered_home_list
            

def parse_price_based_on_base(price_str) -> int | float:
    if "." in price_str:
        return float(price_str)
    elif price_str == '':
        return 0
    else:
        return int(price_str)

def divide_into_bactches(sendable_home_list:list, threshold:int = 8) -> list:
    sendable_size = len(sendable_home_list)
    batches = sendable_size / threshold
    if "." in str(batches):
        batches = batches + 1
    batches = int(batches)
    begin_idx = 0
    end_idx = threshold
    batch_list = []
    for x in range(0,batches):
        new_list = sendable_home_list[begin_idx:end_idx]
        if len(new_list) > 0:
            batch_list.append(new_list)
        begin_idx = end_idx
        end_idx = end_idx + threshold
        
    return batch_list

if __name__ == "__main__":
    address = "Ring road-Kruiskamp 90 L,Amersfoort"
    city = parse_city_string(address)
    print(city)  # Output: The Hague ('s-Gravenhage)