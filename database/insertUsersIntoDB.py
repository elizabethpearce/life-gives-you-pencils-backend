import sys
import os
from os.path import abspath, dirname
from dotenv import load_dotenv

load_dotenv()


parent_dir = dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)

from app import create_app, bcrypt
from database.models import db, Users

def insert_new_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Users(username=username, password_hash=hashed_password)

    app = create_app()
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()

if __name__ == '__main__':

    new_username = os.getenv("NEW_USERNAME")
    new_password = os.getenv("NEW_PASSWORD")

    insert_new_user(new_username, new_password)
