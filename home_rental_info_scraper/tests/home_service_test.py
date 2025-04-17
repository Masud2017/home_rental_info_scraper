import unittest
from home_rental_info_scraper.services.home_services import send_whatsapp_notification_on_user_preferences,sanitize_string
from home_rental_info_scraper.models.Home import Home

class HomeServiceTest(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        
        
    # def test_send_whatsapp_notification_on_user_preferences(self):
    #     home = Home(
    #         address="123 Main St",
    #         city="Amsterdam",
    #         url="http://example.com",
    #         agency="Example Agency",
    #         price="150",
    #         image_url="http://example.com/image.jpg",
    #         room_count="2"
    #     )
    #     send_whatsapp_notification_on_user_preferences([home])
        
    def test_sanitize_string(self):
        test_string = "Appartement \'s-Gravenweg,Rotterdam"
        expected_output = "Appartement s-Gravenweg,Rotterdam"
        result = sanitize_string(test_string)
        self.assertEqual(result, expected_output)