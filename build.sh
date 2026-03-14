#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies (already handled by Render if you use their auto-features, but good for custom scripts)
pip install -r requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# Run migrations automatically
python manage.py migrate
