from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientOut
from app.crud import ingredient as crud

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.post("/", response_model=IngredientOut)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db, ingredient)

@router.get("/", response_model=List[IngredientOut])
def read_all_ingredients(db: Session = Depends(get_db)):
    return crud.get_all_ingredients(db)

@router.get("/{ingredient_id}", response_model=IngredientOut)
def read_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    result = crud.get_ingredient(db, ingredient_id)
    if not result:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return result

@router.put("/{ingredient_id}", response_model=IngredientOut)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate, db: Session = Depends(get_db)):
    result = crud.update_ingredient(db, ingredient_id, ingredient)
    if not result:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return result

@router.delete("/{ingredient_id}", response_model=IngredientOut)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    result = crud.delete_ingredient(db, ingredient_id)
    if not result:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return result
