from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
MONGO_URL = "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@rosentestdata.ky0vl7x.mongodb.net/?retryWrites=true&w=majority+&ssl=true&ssl_cert_reqs=CERT_NONE"

async def connect():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URL)
        return {"message": "Connection successful"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def health_check():
    try:
        client = MongoClient(MONGO_URL)
        return {"message": "Connection successful"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}
