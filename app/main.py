import shutil
import zipfile
from fastapi import FastAPI, UploadFile
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from data_prep import convert_h5_to_json
from pathlib2 import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

origins = [
    "http://localhost",
    "https://localhost",
    "https://bigdata-testing123.firebaseapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

username = "dbUserBigData"
passwort = "Test123123Test"
MONGO_URL = "mongodb+srv://dbUserBigData:Test123123Test@rosentestdata.ky0vl7x.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client["bigdata"]
collection = db["Sensordaten"]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    try:
        client = MongoClient(MONGO_URL)
        return {"message": "Connection successful"}
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}
    
def is_folder(filename):
    # Use pathlib library to detect folder
    return Path(filename).is_dir()

def process_file(filename):
    # Convert data
    try:
        converted_data = convert_h5_to_json(filename)
        # Insert data into MongoDB
        collection.insert_one(converted_data)
        return converted_data
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False

@app.post("/upload")
async def upload_and_convert(file: UploadFile = None):

    if file is not None:
        filename=file.filename
        with filename as f:
            data = f.read()
        return {"filename": filename, "data": data}
        await process_file(file.filename)     
    else:
        # Handle unexpected input combination
        return {"error": "Invalid file or folder combination"}

@app.get("/data")
async def get_data():
    try:
        indexes = collection.list_indexes()
        for index in indexes:
            return("Index name:", index["name"])
    except Exception as e:
        return {"message": "Connection failed: {}".format(e)}
