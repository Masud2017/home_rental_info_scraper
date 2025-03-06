import unittest
from home_rental_info_scraper.models.Home import Home
from home_rental_info_scraper.utils.util import filter_sendable_home_list, parse_price_based_on_base,divide_into_bactches


class TestUtil(unittest.TestCase):
    def test_filter_sendable_home_list(self):
        sample_home = Home(address="some value", city = "some city", url = "dsfsd", agency = "sdf", price = "324", image_url= "sdafad" , room_count= "34")
        sample_home2 = Home(address="some value", city = "some city", url = "dsfsd", agency = "sdf", price = "324", image_url= "sdafad" , room_count= "")
        sample_home3 = Home(address="some value", city = "some city", url = "dsfsd", agency = "sdf", price = "324", image_url= "sdafad" , room_count= "34")
        sample_home4 = Home(address="some value", city = "some city", url = "dsfsd", agency = "sdf", price = "324", image_url= "" , room_count= "34")
        sample_home5 = Home(address="", city = "some city", url = "dsfsd", agency = "sdf", price = "324", image_url= "sdafad" , room_count= "34")
        sample_home6 = Home(address="some value", city = "", url = "dsfsd", agency = "sdf", price = "324", image_url= "sdafad" , room_count= "34")
        sample_home7 = Home(address="some value", city = "some city", url = "", agency = "sdf", price = "324", image_url= "sdafad" , room_count= "34")
        sample_home8 = Home(address="some value", city = "some city", url = "dsfsd", agency = "", price = "324", image_url= "sdafad" , room_count= "34")
        sample_home9 = Home(address="some value", city = "some city", url = "dsfsd", agency = "sdf", price = "", image_url= "sdafad" , room_count= "34")
        
        sample_data = [sample_home, sample_home2, sample_home3, sample_home4, sample_home5, sample_home6,sample_home7, sample_home8, sample_home9]
        expected = [sample_home, sample_home3]
        
        actual = filter_sendable_home_list(sample_data)
        
        self.assertEqual(len(expected), len(actual))
        
    
    def test_parse_price_based_on_base(self):
        source_float = "223.35"
        source_int = "343"
        
        expected_float = 223.35
        expected_int = 343
        
        actual_float = parse_price_based_on_base(source_float)
        actual_int = parse_price_based_on_base(source_int)
        
        self.assertEqual(expected_float,actual_float)
        self.assertEqual(expected_int,actual_int)
    
    
    def test_divide_into_bactches(self):
        source = [34,234,223,4345,46,345,13,234,45,234,645,243,234,5435]
        _threshold = 5
        expected = [[34,234,223],[4345,46,345],[13,234,45],[234,645,243],[234,5435]]
        actual = divide_into_bactches(source,threshold=_threshold)
        
        print(f"expected : {expected}")
        print(f"actual: {actual}")
            
if __name__ == "__main__":
    unittest.main()