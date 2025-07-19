from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate
from app.crud.ingredient import create_ingredient
from app.dependencies import templates

router = APIRouter()

@router.get("/create-ingredient", response_class=HTMLResponse)
def new_ingredient_form(request: Request):
    return templates.TemplateResponse("ingredients/add.html", {"request": request})

@router.post("/create-ingredient")
def create_ingredient_from_form(
    request: Request,
    name: str = Form(...),
    calories: float = Form(...),
    protein: float = Form(...),
    fat: float = Form(...),
    carbs: float = Form(...),
    db: Session = Depends(get_db)
):
    ingredient_data = IngredientCreate(
        name=name,
        calories=calories,
        protein=protein,
        fat=fat,
        carbs=carbs,
    )
    create_ingredient(db, ingredient_data)
    return RedirectResponse(url="/ingredients", status_code=303)

@router.get("/ingredients", response_class=HTMLResponse)
def list_ingredients(request: Request, db: Session = Depends(get_db)):
    ingredients = db.query(Ingredient).all()
    return templates.TemplateResponse("ingredients/list.html", {
        "request": request,
        "ingredients": ingredients,
    })


@router.get("/ingredients/edit/{ingredient_id}", response_class=HTMLResponse)
def edit_ingredient_form(ingredient_id: int, request: Request, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).get(ingredient_id)
    return templates.TemplateResponse("ingredients/edit.html", {
        "request": request,
        "ingredient": ingredient,
    })


@router.post("/ingredients/edit/{ingredient_id}")
def update_ingredient(
    ingredient_id: int,
    name: str = Form(...),
    calories: float = Form(...),
    protein: float = Form(...),
    fat: float = Form(...),
    carbs: float = Form(...),
    db: Session = Depends(get_db)
):
    ingredient = db.query(Ingredient).get(ingredient_id)
    ingredient.name = name
    ingredient.calories = calories
    ingredient.protein = protein
    ingredient.fat = fat
    ingredient.carbs = carbs
    db.commit()
    return RedirectResponse(url="/ingredients", status_code=303)

@router.post("/ingredients/delete/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).get(ingredient_id)
    db.delete(ingredient)
    db.commit()
    return RedirectResponse(url="/ingredients", status_code=303)
