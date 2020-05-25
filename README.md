# Udacity Fullstack Nanodegree Capstone

Preview at https://alexparra-fsnd-capstone.herokuapp.com/

## Users

- Executive Producer: `executive.producer@fsnd-capstone.alex-parra.com`
  Permissions: actors:list, actors:create, actors:update, actors:delete, movies:list, movies:create, movies:update, movies:delete
- Casting Director: `casting.director@fsnd-capstone.alex-parra.com`
  Permissions: actors:list, actors:create, actors:update, actors:delete, movies:list, movies:update
- Casting Assistant: `casting.assistant@fsnd-capstone.alex-parra.com`
  Permissions: actors:list, movies:list

```
FSNDCapstone1q2w3e
```

## App Development

1. VirtualEnv: `python -m venv venv`
2. Activate Env: `source ./venv/bin/activate`
3. Upgrade pip: `python -m pip install pip --upgrade`
4. Install Gunicorn: `python -m pip install gunicorn`
5. Install Flask: `python -m pip install flask`
6. Install Flask-SQLAlchemy: `python -m pip install flask-sqlalchemy`
7. Install psycopg2: `python -m pip install psycopg2-binary`
8. Install Flask-Migrate: `python -m pip install Flask-Migrate`
9. Install Flask-CORS: `python -m pip install flask-cors`
10. Install Flask-JSONSchema: `python -m pip install flask-jsonschema-validator`
11. Install Pythonenv: `python -m pip install python-dotenv`
12. Install Python Jose: `python -m pip install python-jose-cryptodome`
13. Requirements.txt: `python -m pip freeze > requirements.txt`
14. Add .flaskenv with `FLASK_APP`, `FLASK_RUN_HOST`, `FLASK_RUN_PORT`
15. Start DB: `docker-compose up` or `sh boot.sh db-up`
16. Init Migrations: `flask db init`
17. Create Migrations: `flask db migrate`
18. Upgrade DB: `flask db upgrade`
    Downgrade DB: `flask db downgrade`
19. Run dev mode: `sh ./boot.sh dev`

## Setup Heroku

1. Install Heroku CLI: `brew install heroku/brew/heroku`
2. Login to Heroku: `heroku login`
3. Create app at Heroku: `heroku create my-app-name`
4. Set Procfile: `echo "web: gunicorn app:APP" > Procfile`
5. Commit changes and push to origin
6. Push to Heroku: `git push heroku master`
7. Add Postgres DB: `heroku addons:create heroku-postgresql:hobby-dev`
8. At Heroku, DB connection url is taken from env var `DATABASE_URL`
9. Upgrade DB: `heroku run flask db upgrade`
