echo "Building the Project ..."
python -m pip install -r requirements

echo "Make Migrattion..."
python manage.py  makemigrations --noinput
python manage.py  migrate --noinput

echo "Collect Static..."
python manage.py collectstatic --noinput --clear