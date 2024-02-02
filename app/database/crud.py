from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
MONGO_URL = "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@rosentestdata.ky0vl7x.mongodb.net/?retryWrites=true&w=majority+&ssl=true&ssl_cert_reqs=CERT_NONE"
client=MongoClient(MONGO_URL)

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

    
async def get_data():
    try:
        # Get data from MongoDB
        data = client["your_database"].collection.find()
        return {"data": data}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def post_data():
    try:
        # Post data to MongoDB
        client["your_database"].collection.insert_one({"message": "Data posted"})
        return {"message": "Data posted"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def delete_data():
    try:
        # Delete data from MongoDB
        client["your_database"].collection.delete_one({"message": "Data posted"})
        return {"message": "Data deleted"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}
    
async def update_data():
    try:
        # Update data in MongoDB
        client["your_database"].collection.update_one({"message": "Data posted"}, {"$set": {"message": "Data updated"}})
        return {"message": "Data updated"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def patch_data():
    try:
        # Patch data in MongoDB
        client["your_database"].collection.update_one({"message": "Data posted"}, {"$set": {"message": "Data patched"}})
        return {"message": "Data patched"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}
    
async def get_data_by_id(id: str):
    try:
        # Get data from MongoDB by id
        data = client["your_database"].collection.find_one({"_id": id})
        return {"data": data}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def post_data_by_id(id: str):
    try:
        # Post data to MongoDB by id
        client["your_database"].collection.insert_one({"_id": id, "message": "Data posted"})
        return {"message": "Data posted"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def delete_data_by_id(id: str):
    try:
        # Delete data from MongoDB by id
        client["your_database"].collection.delete_one({"_id": id})
        return {"message": "Data deleted"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def update_data_by_id(id: str):
    try:
        # Update data in MongoDB by id
        client["your_database"].collection.update_one({"_id": id}, {"$set": {"message": "Data updated"}})
        return {"message": "Data updated"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}

async def patch_data_by_id(id: str):
    try:
        # Patch data in MongoDB by id
        client["your_database"].collection.update_one({"_id": id}, {"$set": {"message": "Data patched"}})
        return {"message": "Data patched"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}
