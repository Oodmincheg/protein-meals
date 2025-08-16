from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association Table for many-to-many relation between Meal and Ingredient
meal_ingredient_table = Table(
    'meal_ingredients', Base.metadata,
    Column('meal_id', Integer, ForeignKey('meals.id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key=True),
    Column('quantity', Float, nullable=False)  # quantity in grams or other unit
)

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    allergens = Column(String)  # comma-separated string or use a separate table

    def __repr__(self):
        return f"<Ingredient(name={self.name})>"

class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    ingredients = relationship('Ingredient', secondary=meal_ingredient_table, backref='meals')

    def __repr__(self):
        return f"<Meal(name={self.name})>"

