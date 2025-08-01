from fastapi import FastAPI
from app.routers import meals, ingredients, meal_ingredients, ingredients_html
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

app.include_router(meals.router)
app.include_router(ingredients.router)
app.include_router(meal_ingredients.router)
app.include_router(ingredients_html.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"message": "Protein Meals API is running"}
