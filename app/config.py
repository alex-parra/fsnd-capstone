import os

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

AUTH_DOMAIN = os.environ.get("AUTH_DOMAIN")
AUTH_CLIENT_ID = os.environ.get("AUTH_CLIENT_ID")
AUTH_AUDIENCE = os.environ.get("AUTH_AUDIENCE")

TESTING_JWT_KEY = 'capstoneTesting'
