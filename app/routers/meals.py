from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, insert
from typing import List
from starlette.status import HTTP_303_SEE_OTHER

from app.database import get_db
from app.crud.meal import get_meal_summaries
from app.schemas.meal import MealSummary, MealCreate, MealUpdate, MealOut, MealWithIngredients
from app.crud import meal as crud
from app.models.meal import Meal
from app.models.ingredient import Ingredient
from app.models.meal_ingredient import MealIngredient
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/meals", tags=["meals"])
templates = Jinja2Templates(directory="app/templates")

# HTML routes first
@router.get("/html", response_class=HTMLResponse)
def read_all_meals_html(request: Request, db: Session = Depends(get_db)):
    meals = crud.get_all_meals(db)
    return templates.TemplateResponse("meals/list.html", {"request": request, "meals": meals})

@router.get("/add", response_class=HTMLResponse, name="meals.add_meal_form")
def add_meal_form(request: Request):
    return templates.TemplateResponse("meals/add.html", {"request": request})

@router.post("/create", name="meals.create_meal_form")
def create_meal_form(
    name: str = Form(...),
    calories: float = Form(...),
    protein: float = Form(...),
    fat: float = Form(...),
    carbs: float = Form(...),
    db: Session = Depends(get_db)
):
    stmt = insert(Meal).values(
        name=name,
        calories=calories,
        protein=protein,
        fat=fat,
        carbs=carbs
    )
    db.execute(stmt)
    db.commit()
    return RedirectResponse("/meals/html", status_code=HTTP_303_SEE_OTHER)

@router.get("/edit/{meal_id}", response_class=HTMLResponse)
def edit_meal_form(meal_id: int, request: Request, db: Session = Depends(get_db)):
    meal = crud.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return templates.TemplateResponse("meals/edit.html", {"request": request, "meal": meal})

@router.post("/update/{meal_id}")
def update_meal_form(meal_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    updated = crud.update_meal(db, meal_id, MealUpdate(name=name))
    if not updated:
        raise HTTPException(status_code=404, detail="Meal not found")
    return RedirectResponse(url="/meals/html", status_code=HTTP_303_SEE_OTHER)

@router.post("/delete/{meal_id}")
def delete_meal_form(meal_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_meal(db, meal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Meal not found")
    return RedirectResponse(url="/meals/html", status_code=HTTP_303_SEE_OTHER)

# JSON API endpoints
@router.get("/summary", response_model=List[MealSummary])
def read_meal_summaries(db: Session = Depends(get_db)):
    results = get_meal_summaries(db)
    return [dict(row._mapping) for row in results]

@router.get("/summary/html", response_class=HTMLResponse)
def read_meal_summaries_html(request: Request, db: Session = Depends(get_db)):
    results = get_meal_summaries(db)
    meals = [dict(row._mapping) for row in results]
    return templates.TemplateResponse("meals.html", {"request": request, "meals": meals})

@router.get("/filter-by-ingredient", response_model=List[MealWithIngredients])
def filter_meals_by_ingredient(ingredient_name: str, db: Session = Depends(get_db)):
    meals = (
        db.query(Meal)
        .join(Meal.ingredient_links)
        .join(MealIngredient.ingredient)
        .filter(func.lower(Ingredient.name).like(f"%{ingredient_name.lower()}%"))
        .options(joinedload(Meal.ingredient_links).joinedload(MealIngredient.ingredient))
        .distinct()
        .all()
    )
    return meals

@router.post("/", response_model=MealOut)
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    return crud.create_meal(db, meal)

@router.get("/", response_model=List[MealOut])
def read_all_meals(db: Session = Depends(get_db)):
    return crud.get_all_meals(db)

@router.get("/{meal_id}", response_model=MealOut)
def read_meal(meal_id: int, db: Session = Depends(get_db)):
    result = crud.get_meal(db, meal_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meal not found")
    return result

@router.put("/{meal_id}", response_model=MealOut)
def update_meal(meal_id: int, meal: MealUpdate, db: Session = Depends(get_db)):
    result = crud.update_meal(db, meal_id, meal)
    if not result:
        raise HTTPException(status_code=404, detail="Meal not found")
    return result

@router.delete("/{meal_id}", response_model=MealOut)
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    result = crud.delete_meal(db, meal_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meal not found")
    return result
