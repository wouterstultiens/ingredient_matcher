import random
from app import app
from models import Recipe, Ingredient, RecipeStep
from config import db

# Pools of sample data
recipe_names = ["Spaghetti Bolognese", "Chicken Curry", "Vegetable Stir Fry", "Beef Stew", "Tomato Soup", "Caesar Salad", "Grilled Cheese Sandwich", "Pepperoni Pizza", "Pancakes", "Fish Tacos"]
ingredients_pool = [
    {"name": "spaghetti", "amount": "200g"},
    {"name": "chicken", "amount": "200g"},
    {"name": "carrots", "amount": "100g"},
    {"name": "tomatoes", "amount": "150g"},
    {"name": "lettuce", "amount": "50g"},
    {"name": "cheese", "amount": "100g"},
    {"name": "pepperoni", "amount": "70g"},
    {"name": "flour", "amount": "200g"},
    {"name": "fish", "amount": "150g"},
    {"name": "tortilla", "amount": "2 pieces"}
]
steps_pool = [
    "Boil water",
    "Fry on pan",
    "Bake in oven",
    "Mix ingredients",
    "Chop vegetables",
    "Grill on barbecue",
    "Marinate overnight",
    "Simmer on low heat",
    "Whisk together",
    "Serve with sauce"
]

def add_sample_recipes(n):
    for _ in range(n):
        name = random.choice(recipe_names)
        ingredients = [Ingredient(name=ingredient["name"], amount=ingredient["amount"]) for ingredient in random.sample(ingredients_pool, 3)]
        steps = [RecipeStep(step=step) for step in random.sample(steps_pool, 3)]

        recipe = Recipe(name=name, type="dinner", ingredients=ingredients, steps=steps)
        db.session.add(recipe)

    db.session.commit()

with app.app_context():
    add_sample_recipes(10)  # Specify number of recipes to add
