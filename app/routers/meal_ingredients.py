from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from app.database import get_db
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter(prefix="/meal-ingredients", tags=["meal-ingredients"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def list_meal_ingredients(request: Request, db: Session = Depends(get_db)):
    results = (
        db.query(MealIngredient, Meal.name.label("meal_name"), Ingredient.name.label("ingredient_name"))
        .join(Meal, Meal.id == MealIngredient.meal_id)
        .join(Ingredient, Ingredient.id == MealIngredient.ingredient_id)
        .all()
    )
    return templates.TemplateResponse("meal_ingredients/list.html", {"request": request, "meal_ingredients": results})

@router.get("/add", response_class=HTMLResponse)
def add_meal_ingredient_form(request: Request, db: Session = Depends(get_db)):
    meals = db.query(Meal).all()
    ingredients = db.query(Ingredient).all()
    return templates.TemplateResponse("meal_ingredients/add.html", {
        "request": request,
        "meals": meals,
        "ingredients": ingredients
    })

@router.post("/create")
def create_meal_ingredient(
    meal_id: int = Form(...),
    ingredient_id: int = Form(...),
    amount_grams: int = Form(...),
    db: Session = Depends(get_db)
):
    stmt = insert(MealIngredient).values(meal_id=meal_id, ingredient_id=ingredient_id, amount_grams=amount_grams)
    db.execute(stmt)
    db.commit()
    return RedirectResponse("/meal-ingredients", status_code=HTTP_303_SEE_OTHER)

@router.get("/edit/{meal_id}/{ingredient_id}", response_class=HTMLResponse)
def edit_meal_ingredient_form(meal_id: int, ingredient_id: int, request: Request, db: Session = Depends(get_db)):
    result = db.execute(
        select(MealIngredient.amount_grams)
        .where(MealIngredient.meal_id == meal_id)
        .where(MealIngredient.ingredient_id == ingredient_id)
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="MealIngredient not found")

    return templates.TemplateResponse("meal_ingredients/edit.html", {
        "request": request,
        "meal_id": meal_id,
        "ingredient_id": ingredient_id,
        "grams": result[0]
    })

@router.post("/update/{meal_id}/{ingredient_id}")
def update_meal_ingredient(
    meal_id: int,
    ingredient_id: int,
    grams: int = Form(...),
    db: Session = Depends(get_db)
):
    stmt = (
        update(MealIngredient)
        .where(MealIngredient.meal_id == meal_id)
        .where(MealIngredient.ingredient_id == ingredient_id)
        .values(amount_grams=grams)
    )
    db.execute(stmt)
    db.commit()
    return RedirectResponse("/meal-ingredients", status_code=HTTP_303_SEE_OTHER)

@router.post("/delete/{meal_id}/{ingredient_id}")
def delete_meal_ingredient(meal_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    stmt = (
        delete(MealIngredient)
        .where(MealIngredient.meal_id == meal_id)
        .where(MealIngredient.ingredient_id == ingredient_id)
    )
    db.execute(stmt)
    db.commit()
    return RedirectResponse("/meal-ingredients", status_code=HTTP_303_SEE_OTHER)