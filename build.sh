#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py cargar_premium_cnsc_2026
python manage.py apply_market_ready_upgrade
