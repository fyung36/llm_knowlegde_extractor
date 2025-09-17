from fastapi import FastAPI
from src.core.routers import register_routers

def register_core(app: FastAPI):
    register_routers(app)

    @app.get("/ping")
    async def ping():
        return {"message": "pong!"}
