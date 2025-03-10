import psycopg2   
from dotenv import load_dotenv
import os

load_dotenv()                                                                                                        

DB = { 
    "database": os.environ["db_name"],
    "host": os.environ["db_host"],
    "user": os.environ["db_user"],
    "password": os.environ["db_password"],
    "port": os.environ["db_port"]
}

MAIL_GUN_API = os.environ["mail_gun_api"]
MAIL_GUN_API_URL = os.environ["mail_gun_api_url"]
MAIL_GUN_FROM_EMAIL_ADDRESS = os.environ["mail_gun_from_email_address"]