# Udacity Fullstack Nanodegree Capstone

Preview at https://alexparra-fsnd-capstone.herokuapp.com/

# App Steps

1. VirtualEnv: `python -m venv venv`
2. Activate Env: `source ./venv/bin/activate`
3. Upgrade pip: `python -m pip install pip --upgrade`
4. Install Gunicorn: `python -m pip install gunicorn`
5. Install Flask: `python -m pip install flask`
6. Install Flask-SQLAlchemy: `python -m pip install flask-sqlalchemy`
7. Install Flask-CORS: `python -m pip install flask-cors`
8. Install Pythonenv: `python -m pip install python-dotenv`
9. Requirements.txt: `python -m pip freeze > requirements.txt`
10. Add .flaskenv with FLASK_APP, FLASK_RUN_HOST, FLASK_RUN_PORT
11. Run dev mode: `sh ./boot.sh dev`

## Setup Heroku

1. Install Heroku CLI: `brew install heroku/brew/heroku`
2. Login to Heroku: `heroku login`
3. Create app at Heroku: `heroku create my-app-name`
4. Set Procfile: `echo "web: gunicorn app:APP" > Procfile`
5. Commit changes and push to origin
6. Push to Heroku: `git push heroku master`
