# tests/test_meals.py
from app.models.ingredient import Ingredient
from app.models.meal import Meal

def test_compose_meal_calculates_macros(client, db_session):
    # Seed ingredients (per 100g)
    i1 = Ingredient(name="Rice", calories=130, protein=2.7, fat=0.3, carbs=28)
    i2 = Ingredient(name="Chicken", calories=165, protein=31,  fat=3.6, carbs=0)
    db_session.add_all([i1, i2])
    db_session.commit()
    db_session.refresh(i1)
    db_session.refresh(i2)

    # Compose payload: 150g rice + 120g chicken
    payload = {
        "name": "Chicken & Rice",
        "items": [
            {"ingredient_id": i1.id, "amount_grams": 150},
            {"ingredient_id": i2.id, "amount_grams": 120}
        ]
    }

    # DEBUG: list registered routes
    print("ROUTES:", [getattr(r, "path", None) for r in client.app.routes])
    r = client.post("/meal-ingredients/compose", json=payload)

    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Chicken & Rice"

    # Validate totals (rounded in your route to 2 decimals)
    # Rice 150g: factor 1.5 -> cal 195, pro 4.05, fat 0.45, carb 42
    # Chicken 120g: factor 1.2 -> cal 198, pro 37.2, fat 4.32, carb 0
    # Totals: cal 393, pro 41.25, fat 4.77, carbs 42
    assert abs(body["calories"] - 393.0) < 0.01
    assert abs(body["protein"] - 41.25) < 0.01
    assert abs(body["fat"] - 4.77) < 0.01
    assert abs(body["carbs"] - 42.0) < 0.01
    assert len(body["ingredients"]) == 2

def test_compose_meal_missing_ingredient_returns_404(client, db_session):
    # No ingredients seeded -> should fail
    payload = {
        "name": "Ghost Meal",
        "items": [{"ingredient_id": 9999, "amount_grams": 50}]
    }
    r = client.post("/meal-ingredients/compose", json=payload)
    assert r.status_code == 404
    assert "missing_ingredient_ids" in r.json()["detail"]


def test_meal_name_conflict_returns_409(client, db_session):
    # Seed a meal with the conflicting name using ORM (respects __tablename__ = "meal")
    existing = Meal(name="Unique Name", calories=0, protein=0, fat=0, carbs=0)
    db_session.add(existing)

    # Seed one ingredient so the compose request passes validation (items >= 1)
    ing = Ingredient(name="Dummy", calories=100, protein=10, fat=5, carbs=8)
    db_session.add(ing)

    db_session.commit()
    db_session.refresh(ing)

    payload = {
        "name": "Unique Name",  # same as existing -> should hit 409 branch in your route
        "items": [{"ingredient_id": ing.id, "amount_grams": 10}]
    }

    r = client.post("/meal-ingredients/compose", json=payload)
    assert r.status_code == 409