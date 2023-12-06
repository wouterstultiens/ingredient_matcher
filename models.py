from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    # Add more fields as necessary

    def __repr__(self):
        return f'<Recipe {self.name}>'