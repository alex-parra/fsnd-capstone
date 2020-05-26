# Udacity Fullstack Nanodegree Capstone

Final project for the Udacity Fullstack Nanodegree.

> The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

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

## Setup locally for developemt

1. clone this repo and cd into it
2. activate virtual env: `source ./venv/bin/activate`
3. Upgrade pip: `python -m pip install pip --upgrade`
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Start DB: `docker-compose up` or `sh boot.sh db-up`
6. Upgrade DB: `flask db upgrade`
7. Run dev mode: `sh ./boot.sh dev`
8. Open http://localhost:8000/
9. Run tests: `sh boot.sh test`

## Endpoints

`GET /`

- Returns app scafold html

`GET /health`

- Get system health check

`GET /user`

- Get user permissions

`GET /movies`

- Get all Movies
- Requires Auth + `movies:list`
- Response: `{ movies: MOVIE_DTO[] }`

`POST /movies`

- Create a Movie
- Requires Auth + `movies:create`
- Request payload: `See app.schemas.movie.create`
- Response: `{ movie: MOVIE_DTO }`

`PATCH /movies/:id`

- Update a Movie
- Requires Auth + `movies:update`
- Request payload: `See app.schemas.movie.update`
- Response: `{ movie: MOVIE_DTO }`

`DELETE /movies/:id`

- Delete a Movie
- Requires Auth + `movies:delete`
- Response: `{ deleted: MOVIE_DTO }`

`GET /actors`

- Get all Actors
- Requires Auth + `actors:list`
- Response: `{ actors: ACTOR_DTO[] }`

`POST /actors`

- Create an Actor
- Requires Auth + `actors:create`
- Request payload: `See app.schemas.actor.create`
- Response: `{ actor: ACTOR_DTO }`

`PATCH /actors/:id`

- Update an Actor
- Requires Auth + `actors:update`
- Request payload: `See app.schemas.actor.update`
- Response: `{ actor: ACTOR_DTO }`

`DELETE /actors/:id`

- Delete an Actor
- Requires Auth + `actors:delete`
- Response: `{ deleted: ACTOR_DTO }`

`POST /movies/:id/actors`

- Add an Actor to a movie
- Requires Auth + `movies:update`
- Request payload: `{ actor: { id: number } }`
- Response: `{ movie: MOVIE_DTO }`

`DELETE /movies/:id/actors`

- Remove an Actor from a movie
- Requires Auth + `movies:update`
- Request payload: `{ actor: { id: number } }`
- Response: `{ movie: MOVIE_DTO }`

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
10. Install Pythonenv: `python -m pip install python-dotenv`
11. Install Python Jose: `python -m pip install python-jose-cryptodome`
12. Requirements.txt: `python -m pip freeze > requirements.txt`
13. Add .flaskenv with `FLASK_APP`, `FLASK_RUN_HOST`, `FLASK_RUN_PORT`
14. Start DB: `docker-compose up` or `sh boot.sh db-up`
15. Init Migrations: `flask db init`
16. Create Migrations: `flask db migrate`
17. Upgrade DB: `flask db upgrade`
    Downgrade DB: `flask db downgrade`
18. Run dev mode: `sh ./boot.sh dev`

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
