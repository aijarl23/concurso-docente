#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_modulos
python manage.py apply_market_ready_upgrade
python manage.py activar_banco_tjs
python manage.py repair_text_quality
