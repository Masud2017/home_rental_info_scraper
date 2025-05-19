import unittest
from home_rental_info_scraper.spiders.funda import get_site_key

class TestFunda(unittest.TestCase):
    
    
    def test_get_site_key(self):
        print(f"Printing the site key : {get_site_key("https://www.funda.nl/zoeken/huur")}")