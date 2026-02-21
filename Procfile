web: python manage.py migrate && python manage.py collectstatic --noinput && python populate_data.py && gunicorn plateforme_emploi.wsgi --bind 0.0.0.0:$PORT
