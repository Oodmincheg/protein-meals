# app/routers/meal_ingredients_compose.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List

from app.database import get_db
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient  # association object
from app.schemas.meal_compose import (
    ComposeMealRequest, ComposeMealResponse, MealIngredientContribution
)

router = APIRouter(tags=["Meals & Ingredients"])

@router.post("/meal-ingredients/compose", response_model=ComposeMealResponse, status_code=status.HTTP_201_CREATED)
def compose_meal(payload: ComposeMealRequest, db: Session = Depends(get_db)):
    # 1) Ensure unique meal name
    existing = db.query(Meal).filter(Meal.name == payload.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Meal with name "{payload.name}" already exists.'
        )

    # 2) Fetch all ingredients used in one query
    ingredient_ids = [i.ingredient_id for i in payload.items]
    ingredients: List[Ingredient] = (
        db.query(Ingredient)
        .filter(Ingredient.id.in_(ingredient_ids))
        .all()
    )

    # Validate all IDs exist
    found_ids = {ing.id for ing in ingredients}
    missing = [iid for iid in ingredient_ids if iid not in found_ids]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"missing_ingredient_ids": missing}
        )

    # Build a lookup for quick access
    by_id: Dict[int, Ingredient] = {ing.id: ing for ing in ingredients}

    # 3) Compute meal macros (assuming Ingredient macros are per 100g)
    total_cal = 0.0
    total_pro = 0.0
    total_fat = 0.0
    total_carb = 0.0

    contributions: List[MealIngredientContribution] = []

    for item in payload.items:
        ing = by_id[item.ingredient_id]
        factor = item.amount_grams / 100.0

        cals = (ing.calories or 0.0) * factor
        pros = (ing.protein or 0.0) * factor
        fats = (ing.fat or 0.0) * factor
        carbs = (ing.carbs or 0.0) * factor

        total_cal += cals
        total_pro += pros
        total_fat += fats
        total_carb += carbs

        contributions.append(
            MealIngredientContribution(
                ingredient_id=ing.id,
                ingredient_name=ing.name,
                amount_grams=item.amount_grams,
                calories=round(cals, 2),
                protein=round(pros, 2),
                fat=round(fats, 2),
                carbs=round(carbs, 2),
            )
        )

    # Optional: round totals to 2 decimals
    total_cal = round(total_cal, 2)
    total_pro = round(total_pro, 2)
    total_fat = round(total_fat, 2)
    total_carb = round(total_carb, 2)

    # 4) Create Meal + associations in one transaction
    try:
        meal = Meal(
            name=payload.name,
            calories=total_cal,
            protein=total_pro,
            fat=total_fat,
            carbs=total_carb,
        )
        db.add(meal)
        db.flush()  # get meal.id without committing

        # IMPORTANT: you said you renamed relationship to `ingredient_links`
        # and association object table is MealIngredient with field amount_grams.
        links = []
        for item in payload.items:
            links.append(
                MealIngredient(
                    meal_id=meal.id,
                    ingredient_id=item.ingredient_id,
                    amount_grams=item.amount_grams,
                )
            )

        # You can either append to relationship or bulk add
        # If Meal.ingredient_links is a relationship to MealIngredient:
        # meal.ingredient_links.extend(links)
        db.add_all(links)

        db.commit()
        db.refresh(meal)

    except Exception as e:
        db.rollback()
        raise

    return ComposeMealResponse(
        id=meal.id,
        name=meal.name,
        calories=meal.calories,
        protein=meal.protein,
        fat=meal.fat,
        carbs=meal.carbs,
        ingredients=contributions,
    )
