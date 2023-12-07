from app import app
from models import Recipe
from config import db
import pandas as pd

def add_sample_recipes():
    d = {"id": [1, 2, 3, 4], "name": ["bami", "bami", "nasi", "nasi"], "ingredient": ["mie", "ei", "rijst", "ei"]}
    df = pd.DataFrame(d)

    for index, row in df.iterrows():
        recipe = Recipe(id=row["id"], name=row["name"], ingredient=row["ingredient"])
        db.session.add(recipe)

    db.session.commit()

with app.app_context():
    add_sample_recipes()