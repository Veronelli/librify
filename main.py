from fastapi import APIRouter
from src.config.envs import settings
app = APIRouter()

@app.get("/")
async def root():
    return {"message": "server is running"}