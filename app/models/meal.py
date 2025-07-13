from sqlalchemy import Column, Integer, String
from app.database import Base

class Meal(Base):
    __tablename__ = "meal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
