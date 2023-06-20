from fastapi import FastAPI
from src.config.envs import settings
from src.users.routes import route

app = FastAPI()

app.include_router(route)

@app.get("/")
async def root():
    return {"message": "server is running"}