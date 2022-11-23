#!/usr/bin/env bash
# exit on error
set -o errexit

pip uninstall PyCrypto
pip uninstall PyCryptodome
pip install PyCryptodome

python manage.py collectstatic --no-input
python manage.py migrate