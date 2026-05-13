#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Build Tailwind CSS
npm run build:css

# Build React components
npm run build

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_demo
