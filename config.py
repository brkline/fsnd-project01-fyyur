import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
db_user_name = os.environ.get("DB_USER_NAME")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")

# TODO IMPLEMENT DATABASE URL
DATABASE_URI = f'postgresql://{db_user_name}:{db_password}@{db_host}:{db_port}/{db_name}'

# engine = create_engine(DATABASE_URI)
