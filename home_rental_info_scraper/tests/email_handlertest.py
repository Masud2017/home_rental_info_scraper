import unittest
from home_rental_info_scraper.config.email_handler import EmailHandler
from home_rental_info_scraper.models.Home import Home

class EmailHandlerTest(unittest.TestCase):
    def setUp(self):
        self.email_handler = EmailHandler()
        
        # home = hestia.Home()
        

        
    def test_send_email(self):
        # This is a placeholder for the actual test.
        # You would typically mock the email sending function here.
        home = Home()
        home.address = "1234 Main St"
        home.city = "New York"
        home.price = 1000
        home.agency = "Agency"
        home.url = "https://facebook.com"
        
        homes = [home]
        message = self.email_handler.generate_email_message(homes)
        self.email_handler.send_single_email(to_address="msmasud578@gmail.com",message= message,subject= "New Homes", home_list = homes,home_count=1)