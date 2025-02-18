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