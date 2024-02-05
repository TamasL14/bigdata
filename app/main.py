import shutil
import zipfile
from fastapi import FastAPI, UploadFile, File
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from data_prep import convert_h5_to_json

app = FastAPI()
load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
MONGO_URL = "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@rosentestdata.ky0vl7x.mongodb.net/?retryWrites=true&w=majority+&ssl=true&ssl_cert_reqs=CERT_NONE"
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

def process_file(filename):
    # Convert data
    try:
        converted_data = convert_h5_to_json(filename)
        # Insert data into MongoDB
        collection.insert_one(converted_data)
        return True
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False

@app.post("/upload")
async def upload_and_convert(folder: UploadFile):
    if folder.content_type == "application/zip":  # Assuming folder is zipped
        with zipfile.ZipFile(folder.file) as zip_ref:
            zip_ref.extractall("./temp")  # Extract folder contents temporarily
            folder_path = "./temp"
    else:
        folder_path = folder.filename

    try:
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                # Read file data
                with open(os.path.join(folder_path, filename), "rb") as f:
                    data = f.read()
                # Process and store data
                if not process_file(filename):
                    raise Exception(f"Failed to process {filename}")
        return {"message": "Files uploaded and converted successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Optionally delete temporary folder
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

@app.get("/data")
async def get_data():
    data = collection.find_one()
    return data