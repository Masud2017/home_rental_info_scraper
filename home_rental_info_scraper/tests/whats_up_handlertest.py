import unittest
from home_rental_info_scraper.services.whats_up_handler import WhatsAppHandler

class WhatsUpHandlerTest(unittest.TestCase):
    
    def __init__(self,  methodName = "runTest"):
        super().__init__(methodName=methodName)
        self.whats_up_handler = WhatsAppHandler()
        
        
    def test_send_message(self):
        self.whats_up_handler.send_message("Test message", "8801721600967")