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


def parse_city_string(city_string: str):
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
        print(f"Printing the city : {city}")
        if city.lower() in city_string.lower():
            return city

    return None
# if __name__ == "__main__":
#     print(parse_city_string("Beeldsnijderstraat 107,8043 CR Zwolle"))  # Amsterdam