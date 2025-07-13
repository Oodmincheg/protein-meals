from sqlalchemy import Column, Integer, String
from app.database import Base

class Allergen(Base):
    __tablename__ = "allergen"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
