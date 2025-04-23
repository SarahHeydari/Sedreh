python manage.py wait_for_db

python manage.py migrate

#python manage.py create_superuser_if_none # sara superuser


python manage.py load_tehran  # sara add to load Tehran geojson
python manage.py load_bookshops
gunicorn --workers=12 --reload bookstore.wsgi --bind 0.0.0.0:8000
