import psycopg2   
from dotenv import load_dotenv
import os

load_dotenv()                                                                                                        

DB = { 
    "database": os.environ["db_name"],
    "host": "hestia-database",
    "user": "hestia",
    "password": "<db_user_password>",
    "port" : "5432"
}
