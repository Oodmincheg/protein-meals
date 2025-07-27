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

5. Launch shell script from root of the project, that will create fresh alembic migration and populate database with some ingredients and meals
scripts/reset.sh

6. Start the development server:
uvicorn app.main:app --reload

Server will be avalable at http://localhost:8000
FastAPI endpoints (for CRUD and filters testing) will be avalable at http://localhost:8000/docs#/

Visit /ingredients to add or edit ingredients.
/meals to create a meal and assign its macros.

Current tables schema available at:
https://drive.google.com/file/d/1V73ESHTqTT9KAHH2P6lI_PCqk2xPxzRs/view
