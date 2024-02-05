from fastapi import FastAPI
from app.database import crud

app = FastAPI()

@app.lifespan("startup")
async def startup_event():
    await crud.connect_to_mongo()

@app.get("/health")
async def health_check():
    return await crud.health_check()

