from fastapi import FastAPI
from app.core.config import settings
from app.database import engine
from app.models import user, meal, meal_plan

# Create tables (for development only, use migrations in production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
async def root():
    return {"message": "Protein Meal Generator API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
