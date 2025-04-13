python manage.py wait_for_db

python manage.py migrate

gunicorn --workers=12 --reload bookstore.wsgi --bind 0.0.0.0:8000
