from fastapi import APIRouter

app = APIRouter()

@app.get("/")
async def root():
    return {"message": "server is running"}