from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Protein Meal Generator"
    DATABASE_URL: str = "postgresql://user:password@localhost/protein_meals_db"

    class Config:
        env_file = ".env"

settings = Settings()
