from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

MONGO_URL = "mongodb+srv://dbUserBigData:Aa017jHP0ZuWv4Z2@rosentestdata.ky0vl7x.mongodb.net/?retryWrites=true&w=majority&tlsCAFile=isrgrootx1.pem"
client = MongoClient(MONGO_URL)

@app.get("/health")
async def health_check():
    try:
        # Check if connection to MongoDB is established
        client["your_database"].collection.insert_one({"message": "Connected to MongoDB"})
        return {"message": "Connection successful"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}