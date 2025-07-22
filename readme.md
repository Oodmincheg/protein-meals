Protein project is web-based FastAPI application for managing and tracking protein-rich meals.
Users can create meals, associate ingredients and view nutritional data with filtering support and browser-accessible
forms.

Current features of project are:
CRUD operations for ingredient, meals, meal-ingredient (many-to-many relation)
Filter ingredients by nutrients.
HTML forms and list views via Jinja2 templates.
Database migration with Alembic.
Data population scripts.
Built with FastAPI and SQLAlchemy.

Tech stack:
- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Jinja2 (HTML templates)
- Uvicorn (dev server)

Setup instructions
1. Clone the repository:
git clone https://github.com/Oodmincheg/protein-meals

2. Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Set up PostgreSQL database:
Ubuntu / Debian :
sudo apt update
sudo apt install postgresql-client

macOS (with Homebrew)
brew install libpq
brew link --force libpq

5. Create a database named protein_db and a user admin:
sudo -u postgres psql
CREATE DATABASE protein_db;
CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE protein_db TO admin;

6. Run alembic migrations:
alembic upgrade head

7. Populate the database:
python scripts/seed.py

8. Start the development server:
uvicorn app.main:app --reload

Server will be avalable at http://localhost:8000
FastAPI endpoints (for CRUD and filters testing) will be avalable at http://localhost:8000/docs#/

Visit /ingredients to add or edit ingredients.
/meals to create a meal and assign its macros.
