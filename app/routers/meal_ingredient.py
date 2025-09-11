from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient
from app.schemas.meal_ingredient import (
    MealIngredientCreate, MealIngredientUpdate, MealIngredientOut
)

router = APIRouter(prefix="/meal-ingredients", tags=["MealIngredients"])

def _ensure_meal_and_ingredient(db: Session, meal_id: int, ingredient_id: int) -> None:
    # SQLAlchemy 2.x preferred API
    if db.get(Meal, meal_id) is None:
        raise HTTPException(status_code=404, detail=f"Meal {meal_id} not found")
    if db.get(Ingredient, ingredient_id) is None:
        raise HTTPException(status_code=404, detail=f"Ingredient {ingredient_id} not found")

@router.post("/", response_model=MealIngredientOut, status_code=status.HTTP_201_CREATED)
def link_meal_ingredient(payload: MealIngredientCreate, db: Session = Depends(get_db)):
    # Validate FKs first to avoid generic 500s
    _ensure_meal_and_ingredient(db, payload.meal_id, payload.ingredient_id)

    # Prevent duplicate link (return 409 instead of 500 on unique violations)
    existing = (
        db.query(MealIngredient)
        .filter(
            MealIngredient.meal_id == payload.meal_id,
            MealIngredient.ingredient_id == payload.ingredient_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Link meal_id={payload.meal_id} & ingredient_id={payload.ingredient_id} already exists",
        )

    link = MealIngredient(**payload.model_dump())  # v2: model_dump()
    db.add(link)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # If we somehow hit a DB constraint, map to a friendly error
        raise HTTPException(status_code=409, detail="Integrity error creating link")
    db.refresh(link)
    return link

@router.get("/", response_model=List[MealIngredientOut])
def list_links(db: Session = Depends(get_db)):
    return db.query(MealIngredient).all()

@router.get("/{meal_id}/{ingredient_id}", response_model=MealIngredientOut)
def get_link(meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    link = (
        db.query(MealIngredient)
        .filter(
            MealIngredient.meal_id == meal_id,
            MealIngredient.ingredient_id == ingredient_id,
        )
        .first()
    )
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@router.put("/{meal_id}/{ingredient_id}", response_model=MealIngredientOut)
def update_link(
    meal_id: int,
    ingredient_id: int,
    payload: MealIngredientUpdate,
    db: Session = Depends(get_db),
):
    link = (
        db.query(MealIngredient)
        .filter(
            MealIngredient.meal_id == meal_id,
            MealIngredient.ingredient_id == ingredient_id,
        )
        .first()
    )
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    # Only update grams
    link.amount_grams = payload.amount_grams
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Integrity error updating link")
    db.refresh(link)
    return link

@router.delete("/{meal_id}/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    link = (
        db.query(MealIngredient)
        .filter(
            MealIngredient.meal_id == meal_id,
            MealIngredient.ingredient_id == ingredient_id,
        )
        .first()
    )
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return None
