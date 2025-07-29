from fastapi import FastAPI
from app.routers import meal_ingredient, meals, ingredients
from fastapi.staticfiles import StaticFiles

from fastapi.requests import Request

app = FastAPI()

app.include_router(meals.router)
app.include_router(ingredients.router)
app.include_router(meal_ingredient.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"message": "Protein Meals API is running"}
