# app/routers/meal_ingredient.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.meal_ingredient import MealIngredientCreate, MealIngredientUpdate, MealIngredientOut
from app.crud import meal_ingredient as crud

router = APIRouter(prefix="/meal-ingredients", tags=["Meal Ingredients"])

@router.post("/", response_model=MealIngredientOut)
def create_link(data: MealIngredientCreate, db: Session = Depends(get_db)):
    return crud.create_meal_ingredient(db, data)

@router.get("/", response_model=list[MealIngredientOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_meal_ingredients(db, skip, limit)

@router.get("/{meal_id}/{ingredient_id}", response_model=MealIngredientOut)
def read_link(meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    link = crud.get_meal_ingredient(db, meal_id, ingredient_id)
    if not link:
        raise HTTPException(status_code=404, detail="Meal-Ingredient link not found")
    return link

@router.put("/{meal_id}/{ingredient_id}", response_model=MealIngredientOut)
def update_link(meal_id: int, ingredient_id: int, data: MealIngredientUpdate, db: Session = Depends(get_db)):
    link = crud.update_meal_ingredient(db, meal_id, ingredient_id, data)
    if not link:
        raise HTTPException(status_code=404, detail="Meal-Ingredient link not found")
    return link

@router.delete("/{meal_id}/{ingredient_id}", response_model=MealIngredientOut)
def delete_link(meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    link = crud.delete_meal_ingredient(db, meal_id, ingredient_id)
    if not link:
        raise HTTPException(status_code=404, detail="Meal-Ingredient link not found")
    return link
