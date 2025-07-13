from fastapi import FastAPI
from app.routers import meals

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.include_router(meals.router)

@app.get("/")
def root():
    return {"message": "Protein Meals API is running"}
