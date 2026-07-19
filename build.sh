#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py deduplicar_datos
python manage.py renombrar_arquitectura_institucional
python manage.py seed_modulos
python manage.py apply_market_ready_upgrade
python manage.py repair_text_quality
python manage.py sync_banco_simulacros
