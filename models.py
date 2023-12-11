from config import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(255))
    time_prepare = db.Column(db.String(50))
    time_wait = db.Column(db.String(50))
    rating = db.Column(db.Float)
    tags = db.Column(db.String(255))
    servings = db.Column(db.String(50))
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    steps = db.relationship('RecipeStep', backref='recipe', lazy=True)
    equipment = db.Column(db.String(255))
    image = db.Column(db.String(255))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(50))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

class RecipeStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    order = db.Column(db.Integer)  # To maintain the order of steps