# tests/test_ingredients.py
from app.models.ingredient import Ingredient

def test_create_and_list_ingredients(client, db_session):
    # Create via API (adjust your real route)
    payload = {
        "name": "Chicken Breast",
        "calories": 165.0,
        "protein": 31.0,
        "fat": 3.6,
        "carbs": 0.0
    }
    r = client.post("/ingredients", json=payload)  # adjust route if needed
    assert r.status_code in (200, 201)
    data = r.json()
    assert data["name"] == "Chicken Breast"
    assert data["protein"] == 31.0

    # List
    r = client.get("/ingredients")
    assert r.status_code == 200
    items = r.json()
    assert any(i["name"] == "Chicken Breast" for i in items)

def test_update_ingredient(client, db_session):
    # seed (direct DB insert is fine for setup)
    ing = Ingredient(name="Tomato", calories=18, protein=0.9, fat=0.2, carbs=3.9)
    db_session.add(ing)
    db_session.commit()
    db_session.refresh(ing)

    r = client.put(
        f"/ingredients/{ing.id}",
        json={"name": "Tomato (ripe)", "calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9}
    )   
    assert r.status_code == 200

def test_delete_ingredient(client, db_session):
    ing = Ingredient(name="Onion", calories=40, protein=1.1, fat=0.1, carbs=9.3)
    db_session.add(ing)
    db_session.commit()
    db_session.refresh(ing)

    r = client.delete(f"/ingredients/{ing.id}")
    assert r.status_code in (200, 204)

    r = client.get(f"/ingredients/{ing.id}")
    assert r.status_code in (404, 400)  # depends on your design
