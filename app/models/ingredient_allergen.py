from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class IngredientAllergen(Base):
    __tablename__ = "ingredient_allergen"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id", ondelete="CASCADE"))
    allergen_id = Column(Integer, ForeignKey("allergen.id", ondelete="CASCADE"))
