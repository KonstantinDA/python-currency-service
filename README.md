# python-currency-service
python, fastAPI, Mongo, Docker

## How to run 
- pip install pipenv
- pipenv shell
- pipenv install --system --deploy
- uvicorn route:app --host 0.0.0.0 --port 8000 --reload

## How to run with docker
- docker-compose build
- docker-compose up

## Documentation
- http://localhost:8000/docs
or 
- http://localhost:8000/redoc 