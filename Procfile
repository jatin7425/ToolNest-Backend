web: gunicorn toolnest_backend.wsgi:application --log-file -
worker: celery -A toolnest_backend worker --loglevel=info
