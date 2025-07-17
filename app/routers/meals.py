from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.meal import get_meal_summaries
from app.schemas.meal import MealSummary
from fastapi.templating import Jinja2Templates

from app.schemas.meal import MealCreate, MealUpdate, MealOut
from app.crud import meal as crud

router = APIRouter(prefix="/meals", tags=["meals"])

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="app/templates")

# JSON endpoint
@router.get("/summary", response_model=List[MealSummary])
def read_meal_summaries(db: Session = Depends(get_db)):
    results = get_meal_summaries(db)
    return [dict(row._mapping) for row in results]

# HTML endpoint
@router.get("/summary/html", response_class=HTMLResponse)
def read_meal_summaries_html(request: Request, db: Session = Depends(get_db)):
    results = get_meal_summaries(db)
    meals = [dict(row._mapping) for row in results]
    return templates.TemplateResponse("meals.html", {"request": request, "meals": meals})


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