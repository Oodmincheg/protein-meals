from fastapi import FastAPI
from app.routers import meal_ingredient, meals, ingredients, meal_ingredients_compose
from fastapi.staticfiles import StaticFiles

from fastapi.requests import Request

app = FastAPI(title="Protein Meals API")

app.include_router(meals.router)
app.include_router(ingredients.router)
app.include_router(meal_ingredient.router)
app.include_router(meal_ingredients_compose.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"message": "Protein Meals API is running"}
