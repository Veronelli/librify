from fastapi import APIRouter
from src.config.envs import settings
from src.users.routes import route

app = APIRouter()

app.include_router(route)

@app.get("/")
async def root():
    return {"message": "server is running"}