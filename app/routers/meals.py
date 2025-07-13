from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.meal import get_meal_summaries
from app.schemas.meal import MealSummary
from fastapi.templating import Jinja2Templates

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
