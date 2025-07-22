#!/bin/bash

echo "Dropping and recreating database..."

# Drop and recreate database
sudo -u postgres dropdb --if-exists protein_db
sudo -u postgres createdb protein_db -O admin

# Wipe migration history
rm -rf alembic/versions/*

# Create fresh initial migration
alembic revision --autogenerate -m "Clean migration"
alembic upgrade head

# Seed
python scripts/seed.py

echo "✅ Reset and seed complete."
