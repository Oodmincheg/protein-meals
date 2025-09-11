from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from app.database import get_db
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient
from app.schemas.meal import MealCreate, MealUpdate, MealOut, MealSummary, MealWithIngredients

router = APIRouter(prefix="/meals", tags=["Meals"])


# --------- Summary (for your summary table endpoint) ---------
@router.get("/summary", response_model=List[MealSummary])
def meals_summary(db: Session = Depends(get_db)):
    return db.query(Meal).all()

# --------- Filter by ingredient ---------
@router.get("/filter-by-ingredient", response_model=List[MealOut])
def meals_by_ingredient(
    ingredient_id: Optional[int] = Query(None, gt=0),
    ingredient_name: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db),
):
    if ingredient_id is None and ingredient_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide ingredient_id or ingredient_name."
        )

    q = (
        db.query(Meal)
        .join(MealIngredient, Meal.id == MealIngredient.meal_id)
        .join(Ingredient, Ingredient.id == MealIngredient.ingredient_id)
    )

    if ingredient_id is not None:
        q = q.filter(MealIngredient.ingredient_id == ingredient_id)

    if ingredient_name is not None:
        ilike = f"%{ingredient_name.strip().lower()}%"
        q = q.filter(func.lower(Ingredient.name).like(ilike))  # portable ILIKE

    return q.distinct(Meal.id).all()


# --------- Create ---------
@router.post("/", response_model=MealOut, status_code=status.HTTP_201_CREATED)
def create_meal(payload: MealCreate, db: Session = Depends(get_db)):
    meal = Meal(**payload.model_dump())
    db.add(meal)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # unique name conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Meal with this name already exists")
    db.refresh(meal)
    return meal

# --------- Read (list) ---------
@router.get("/", response_model=List[MealOut])
def list_meals(db: Session = Depends(get_db)):
    meals = db.query(Meal).all()
    return meals

# --------- Read (by id) ---------
@router.get("/{meal_id}", response_model=MealOut)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).get(meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    return meal

# --------- Update (partial) ---------
@router.put("/{meal_id}", response_model=MealOut)
def update_meal(meal_id: int, payload: MealUpdate, db: Session = Depends(get_db)):
    meal = db.query(Meal).get(meal_id)
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    # Only apply provided fields
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(meal, k, v)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Meal with this name already exists")
    db.refresh(meal)
    return meal

# --------- Delete ---------
@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).get(meal_id)
    if not meal:
        # DELETE can be idempotent; 404 is also acceptable — pick one policy.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    db.delete(meal)
    db.commit()
    return None

# --------- Fetch meal with resolved ingredients (if you need it in UI) ---------
@router.get("/{meal_id}/with-ingredients", response_model=MealWithIngredients)
def get_meal_with_ingredients(meal_id: int, db: Session = Depends(get_db)):
    meal = (
        db.query(Meal)
        .options(
            joinedload(Meal.ingredient_links).joinedload(MealIngredient.ingredient)
        )
        .get(meal_id)
    )
    if not meal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    # MealWithIngredients.ingredients expects IngredientOut items; thanks to from_attributes, returning `meal` works.
    return meal