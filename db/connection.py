import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def getConnection():
    return pymysql.connect(
        host=DB_HOST, 
        port=int(DB_PORT), 
        user=DB_USER, 
        password=DB_PASSWORD, 
        database=DB_NAME, 
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )