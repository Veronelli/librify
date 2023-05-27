from fastapi import APIRouter
from src.config import settings
app = APIRouter()

@app.get("/")
async def root():
    return {"message": "server is running"}