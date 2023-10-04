from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)      

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_LOCAL_URI')

    from .models import ForSaleImages

    db.init_app(app)

    with app.app_context():
        db.create_all()

        return app