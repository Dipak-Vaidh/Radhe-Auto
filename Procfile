# Elastic Beanstalk + nginx expect the app on port 8000. (Render: set PORT=8000 or override start command.)
web: gunicorn radhe_cars.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
