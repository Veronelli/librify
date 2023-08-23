from fastapi import FastAPI

from src.users.routes import route as user_route
from src.users.session_routes import route as session_route

app = FastAPI()

app.include_router(user_route)
app.include_router(session_route)


@app.get("/")
async def root():
    return {"message": "server is running"}
