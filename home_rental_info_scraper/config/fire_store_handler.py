import firebase_admin 
from firebase_admin.credentials import Certificate
from firebase_admin import firestore
import os
path =os.path.abspath("home_rental_info_scraper/config/google-services.json")
print(path)

app = firebase_admin.initialize_app(credential= Certificate(path))

db = firestore.client()
db_url = "https://firestore.googleapis.com/v1/projects/home-rental-info/databases/(default)/documents/home_list/" # need to add document id
