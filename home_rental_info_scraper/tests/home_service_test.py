import unittest
from home_rental_info_scraper.services.home_services import send_whatsapp_notification_on_user_preferences

class HomeServiceTest(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        
        
    def test_send_whatsapp_notification_on_user_preferences(self):
        send_whatsapp_notification_on_user_preferences([])