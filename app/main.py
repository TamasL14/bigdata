from fastapi import FastAPI
from app.database import crud

app = FastAPI()

@app.lifespan("startup")
async def startup_event():
    await crud.connect_to_mongo()

@app.get("/")
async def get_data():
    return await crud.get_data()

@app.post("/")
async def post_data():
    return await crud.post_data()

@app.delete("/")
async def delete_data():
    return await crud.delete_data()

@app.put("/")
async def update_data():
    return await crud.update_data()

@app.patch("/")
async def patch_data():
    return await crud.patch_data()

@app.get("/{id}")
async def get_data_by_id(id: str):
    return await crud.get_data_by_id(id)

@app.post("/{id}")
async def post_data_by_id(id: str):
    return await crud.post_data_by_id(id)

@app.delete("/{id}")
async def delete_data_by_id(id: str):
    return await crud.delete_data_by_id(id)

@app.put("/{id}")
async def update_data_by_id(id: str):
    return await crud.update_data_by_id(id)

@app.get("/health")
async def health_check():
    return await crud.health_check()

