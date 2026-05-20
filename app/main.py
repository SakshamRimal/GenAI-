from fastapi import FastAPI
from app.router import router

app = FastAPI(title="Text-to-SQL Agent")

app.include_router(router)