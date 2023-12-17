from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///recipes.db')
    # Other general configuration settings can be added here

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
