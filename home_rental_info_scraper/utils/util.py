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
    else:
        return int(price_str)

# from geopy.geocoders import Nominatim
# def parse_city_string(address):
#     geolocator = Nominatim(user_agent="city_finder")
#     location = geolocator.geocode(address, addressdetails=True)
    
#     if location and 'address' in location.raw:
#         return location.raw['address'].get('city', location.raw['address'].get('town', location.raw['address'].get('village')))

#     return address


if __name__ == "__main__":
    address = "Ring road-Kruiskamp 90 L,Amersfoort"
    city = parse_city_string(address)
    print(city)  # Output: The Hague ('s-Gravenhage)