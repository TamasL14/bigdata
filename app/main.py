import shutil
import zipfile
from fastapi import FastAPI, UploadFile
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from data_prep import convert_h5_to_json
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
MONGO_URL = "mongodb+srv://{}:{}@rosentestdata.ky0vl7x.mongodb.net/?retryWrites=true&w=majority".format(
    username, passwort
)
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
    file_path = f"/tmp/uploads/{filename}.h5"
    if os.path.exists(file_path):
        converted_data = convert_h5_to_json(filename)
        # Insert data into MongoDB
        collection.insert_one(converted_data)
        return converted_data
    else:
        print(f"Error processing {filename}: {e}")
        return False

@app.post("/upload")
async def upload_and_convert(file: UploadFile = None, folder: UploadFile = None):
    if file is None and folder is None:
        # Handle missing input error
        return {"error": "No file or folder uploaded"}
    elif file is not None:
        file_path = f"/tmp/uploads/{file.filename}.h5"
        with open(file_path, "wb") as f:
            await file.read(into=f)
        try:
            process_file(file.filename)
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")  

    elif folder is not None:
        folder_path = f"/tmp/uploads/{folder.filename}"
        # Iterate through files in the folder
        if folder.content_type == "application/zip":  # Assuming folder is zipped
            with zipfile.ZipFile(folder.file) as zip_ref:
                zip_ref.extractall("./temp")  # Extract folder contents temporarily
                folder_path = "./temp"
        else:
            folder_path = f"/tmp/uploads/{folder.filename}"

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
