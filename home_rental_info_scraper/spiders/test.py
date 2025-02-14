import requests
from bs4 import BeautifulSoup
import json
import re


class Home:
    def __init__(self, address: str = '', city: str = '', url: str = '', agency: str = '', price: int = -1, image_url: str = '') -> None:
        self.address = address
        self.city = city
        self.url = url
        self.agency = agency
        self.price = price
        self.image_url = image_url
        
    def __repr__(self) -> str:
        return str(self)
        
    def __str__(self) -> str:
        return f"{self.address}, {self.city} ({self.agency.title()})"
        
    def __eq__(self, other: 'Home') -> bool:
        if self.address.lower() == other.address.lower():
            if self.city.lower() == other.city.lower():
                return True
        return False
    
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
        
    # @city.setter
    # def city(self, city: str) -> None:
    #     # Strip the trailing province if present
    #     if re.search(" \([a-zA-Z]{2}\)$", city):
    #         city = ' '.join(city.split(' ')[:-1])
    
    #     # Handle cities with two names and other edge cases
    #     if city.lower() in ["'s-gravenhage", "s-gravenhage"]:
    #         city = "Den Haag"
    #     elif city.lower() in ["'s-hertogenbosch", "s-hertogenbosch"]:
    #         city = "Den Bosch"
    #     elif city.lower() in ["alphen aan den rijn", "alphen a/d rijn"]:
    #         city = "Alphen aan den Rijn"
    #     elif city.lower() in ["koog aan de zaan", "koog a/d zaan"]:
    #         city = "Koog aan de Zaan"
    #     elif city.lower() in ["capelle aan den ijssel", "capelle a/d ijssel"]:
    #         city = "Capelle aan den IJssel"
    #     elif city.lower() in ["berkel-enschot", "berkel enschot"]:
    #         city = "Berkel-Enschot"
    #     elif city.lower() in ["oud-beijerland", "oud beijerland"]:
    #         city = "Oud-Beijerland"
    #     elif city.lower() in ["etten-leur", "etten leur"]:
    #         city = "Etten-Leur"
    #     elif city.lower() in ["nieuw vennep", "nieuw-vennep"]:
    #         city = "Nieuw-Vennep"
    #     elif city.lower() == "son en breugel":
    #         city = "Son en Breugel"
    #     elif city.lower() == "bergen op zoom":
    #         city = "Bergen op Zoom"
    #     elif city.lower() == "berkel en rodenrijs":
    #         city = "Berkel en Rodenrijs"
    #     elif city.lower() == "wijk bij duurstede":
    #         city = "Wijk bij Duurstede"
    #     elif city.lower() == "hoogvliet rotterdam":
    #         city = "Hoogvliet Rotterdam"
    #     elif city.lower() == "nederhorst den berg":
    #         city = "Nederhorst den Berg"
    #     elif city.lower() == "huis ter heide":
    #         city = "Huis ter Heide"
            
    #     self._parsed_city = city

def parse_alliantie(r: requests.models.Response):
    jsonDataRegex = r'const\s+surveyJson\s*=\s*(\{.*?\});'
    jsonData = re.search(jsonDataRegex, r.text).group(1)
    with open("log2.txt", "w",encoding='utf-8') as f:
        f.write(str(r.content))
    results = json.loads(jsonData)["data"]
    
    for res in results:
        # Filter results not in selection because why the FUCK would you include
        # parameters and then not actually use them in your FUCKING API
        if not res["isInSelection"]:
            continue
            
        home = Home(agency="alliantie")
        home.address = res["address"]
        # this is a dirty hack because what website with rental homes does not
        # include the city AT ALL in their FUCKING API RESPONSES
        city_start = res["url"].index('/') + 1
        city_end = res["url"][city_start:].index('/') + city_start
        home.city = res["url"][city_start:city_end].capitalize()
        home.url = "https://ik-zoek.de-alliantie.nl/" + res["url"].replace(" ", "%20")
        home.price = int(res["price"][2:].replace('.', ''))
        self.homes.append(home)
            
if __name__ == "__main__":
    headers = {}
    req = requests.get("https://ik-zoek.de-alliantie.nl/aanbod?_gl=1*lkt4rw*_gcl_au*MTY5NjczODI4MC4xNzM5Mzg1NTc0*FPAU*MTY5NjczODI4MC4xNzM5Mzg1NTc0*_ga*NjE3NzA3NTQuMTczOTM4NTU3NQ..*_ga_479KG3CQM4*MTczOTUzMDY2NC4zLjAuMTczOTUzMDY3MS4wLjAuMzY3NDQ0Mzkz*_fplc*bTllR0o5WkZ2RnUxUXJwblNkamVwQ0pTSGszWU1MYXRqT21tMGl4Sm5mcE1udkV6d0ZsdHNsRkdZaXBDT0Q0R3B3STVhMHB5Y0VXaGFyUlNHQ0hJRUUlMkJXdGFZS1BNd1N5VHhhUG12T2VYcWpycFF3M2VmbzRPYWM1SzBKM3clM0QlM0Q.")
    parse_alliantie(req)

