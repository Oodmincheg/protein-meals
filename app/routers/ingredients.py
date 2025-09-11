from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientOut
from app.crud import ingredient as crud

from app.models.ingredient import Ingredient

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.post("/", response_model=IngredientOut)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db, ingredient)

@router.get("/", response_model=List[IngredientOut])
def read_all_ingredients(db: Session = Depends(get_db)):
    return crud.get_all_ingredients(db)

@router.get("/ingredients/filter", response_model=List[IngredientOut])
def filter_ingredients(
    min_protein: Optional[float] = Query(None),
    max_protein: Optional[float] = Query(None),
    min_fat: Optional[float] = Query(None),
    max_fat: Optional[float] = Query(None),
    min_carbs: Optional[float] = Query(None),
    max_carbs: Optional[float] = Query(None),
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Ingredient)

    if min_protein is not None:
        query = query.filter(Ingredient.protein >= min_protein)
    if max_protein is not None:
        query = query.filter(Ingredient.protein <= max_protein)
    if min_fat is not None:
        query = query.filter(Ingredient.fat >= min_fat)
    if max_fat is not None:
        query = query.filter(Ingredient.fat <= max_fat)
    if min_carbs is not None:
        query = query.filter(Ingredient.carbs >= min_carbs)
    if max_carbs is not None:
        query = query.filter(Ingredient.carbs <= max_carbs)
    if name:
        query = query.filter(Ingredient.name.ilike(f"%{name}%"))

    return query.all()

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
