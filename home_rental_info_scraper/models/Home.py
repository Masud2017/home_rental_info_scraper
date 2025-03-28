from datetime import datetime
import re

class Home:
    def __init__(self, address: str = '', city: str = '', url: str = '', agency: str = '', price: str = -1, image_url: str = '', room_count:int = 1) -> None:
        self.address = address
        self.city = city
        self.url = url
        self.agency = agency
        self.date_added = datetime.now()
        self.price = price
        self.image_url = image_url
        self.room_count = room_count
        
    def __repr__(self) -> str:
        return str(self)
        
    def __str__(self) -> str:
        
        return f'\'{self.address}\', \'{self.city}\', \'{self.url}\', \'{self.agency}\',\'{self.date_added}\', {self.price}, \'{self.image_url}\', {self.room_count}'
    
        
    def __eq__(self, other: 'Home') -> bool:
        if self.address.lower() == other["address"].lower():
            if self.city.lower() == other["city"].lower() and \
               self.url.lower() == other["url"].lower() and \
               self.agency.lower() == other["agency"].lower() and \
               self.price == other["price"] and \
               self.image_url.lower() == other["image_url"].lower() and \
               self.room_count == other["room_count"]:
                return True
        return False
    def get_home_tuple(self):
        def escape_string(s: str) -> str:
            return s.replace("'", "")

        address = escape_string(self.address if self.address is not None else "")
        city = escape_string(self.city if self.city is not None else "")
        url = escape_string(self.url if self.url is not None else "")
        agency = escape_string(self.agency if self.agency is not None else "")
        price = self.price if self.price is not None else 0
        if self.price == '':
            price = 0
        image_url = escape_string(self.image_url if self.image_url is not None else "")
        room_count = self.room_count if self.room_count is not None else 0
        print(f"Address: {address}")
        print(f"City: {city}")
        print(f"URL: {url}")
        print(f"Agency: {agency}")
        print(f"Price: {price}")
        print(f"Image URL: {image_url}")
        print(f"Room Count: {room_count}")
        return (
            str(address), 
            str(city), 
            str(url), 
            str(agency), 
            str(self.date_added), 
            str(price), 
            str(image_url), 
            str(room_count)
        )
        
        
    @property
    def room_count(self) -> int:
        return self._room_count

    @room_count.setter
    def room_count(self, room_count: int) -> None:
        self._room_count = room_count
    @property
    def address(self) -> str:
        return self._address
        
    @address.setter
    def address(self, address: str) -> None:
        self._address = address
        
    @property
    def city(self) -> str:
        return self._parsed_city
    
    @property
    def image_url(self) -> str:
        return self._image_url
        
    @city.setter
    def city(self, city: str) -> None:
        # Strip the trailing province if present
        # if re.search(" \([a-zA-Z]{2}\)$", city):
        #     city = ' '.join(city.split(' ')[:-1])
    
        # # Handle cities with two names and other edge cases
        # if city.lower() in ["'s-gravenhage", "s-gravenhage"]:
        #     city = "Den Haag"
        # elif city.lower() in ["'s-hertogenbosch", "s-hertogenbosch"]:
        #     city = "Den Bosch"
        # elif city.lower() in ["alphen aan den rijn", "alphen a/d rijn"]:
        #     city = "Alphen aan den Rijn"
        # elif city.lower() in ["koog aan de zaan", "koog a/d zaan"]:
        #     city = "Koog aan de Zaan"
        # elif city.lower() in ["capelle aan den ijssel", "capelle a/d ijssel"]:
        #     city = "Capelle aan den IJssel"
        # elif city.lower() in ["berkel-enschot", "berkel enschot"]:
        #     city = "Berkel-Enschot"
        # elif city.lower() in ["oud-beijerland", "oud beijerland"]:
        #     city = "Oud-Beijerland"
        # elif city.lower() in ["etten-leur", "etten leur"]:
        #     city = "Etten-Leur"
        # elif city.lower() in ["nieuw vennep", "nieuw-vennep"]:
        #     city = "Nieuw-Vennep"
        # elif city.lower() == "son en breugel":
        #     city = "Son en Breugel"
        # elif city.lower() == "bergen op zoom":
        #     city = "Bergen op Zoom"
        # elif city.lower() == "berkel en rodenrijs":
        #     city = "Berkel en Rodenrijs"
        # elif city.lower() == "wijk bij duurstede":
        #     city = "Wijk bij Duurstede"
        # elif city.lower() == "hoogvliet rotterdam":
        #     city = "Hoogvliet Rotterdam"
        # elif city.lower() == "nederhorst den berg":
        #     city = "Nederhorst den Berg"
        # elif city.lower() == "huis ter heide":
        #     city = "Huis ter Heide"
            
        self._parsed_city = city
        
    @property
    def date_added(self) -> datetime:
        return self._date_added

    @date_added.setter
    def date_added(self, date_added: datetime) -> None:
        self._date_added = date_added
    @image_url.setter
    def image_url(self, image_url: str) -> None:
        self._image_url = image_url
        
    def get_tuple(self):
        return (self.url, self.address, self.city, self.price, self.agency, self.image_url, datetime.now().__str__())
        
        
        
# if __name__ == "__main__":
#     home = Home(address="sdrf", city="city", url="http://example.com", agency="agency", price=34, image_url="image_url")
    
#     print(home.get_tuple())