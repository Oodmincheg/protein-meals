from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.meal_ingredient import MealIngredientCreate, MealIngredientUpdate, MealIngredientOut
from app.crud import meal_ingredient as crud

router = APIRouter(prefix="/meal-ingredients", tags=["meal_ingredients"])

@router.post("/", response_model=MealIngredientOut)
def create_mi(mi: MealIngredientCreate, db: Session = Depends(get_db)):
    return crud.create_meal_ingredient(db, mi)

@router.get("/", response_model=List[MealIngredientOut])
def read_all_mi(db: Session = Depends(get_db)):
    return crud.get_all_meal_ingredients(db)

@router.get("/{mi_id}", response_model=MealIngredientOut)
def read_single_mi(mi_id: int, db: Session = Depends(get_db)):
    result = crud.get_meal_ingredient(db, mi_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meal ingredient not found")
    return result

@router.put("/{mi_id}", response_model=MealIngredientOut)
def update_mi(mi_id: int, mi: MealIngredientUpdate, db: Session = Depends(get_db)):
    result = crud.update_meal_ingredient(db, mi_id, mi)
    if not result:
        raise HTTPException(status_code=404, detail="Meal ingredient not found")
    return result

@router.delete("/{mi_id}", response_model=MealIngredientOut)
def delete_mi(mi_id: int, db: Session = Depends(get_db)):
    result = crud.delete_meal_ingredient(db, mi_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meal ingredient not found")
    return result
