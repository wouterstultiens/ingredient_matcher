import csv
import ast  # To safely evaluate strings as Python literals
from models import db, Recipe, Ingredient, RecipeStep
from app import app

def import_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipe = Recipe(
                name=row['name'],
                link=row['link'],
                time_prepare=row['time_prepare'],
                time_wait=row['time_wait'],
                rating=float(row['rating']) if row['rating'] else None,
                rating_count=int(row['rating_count']) if row['rating_count'] else 0,
                tags=row['tags'],
                servings=row['servings'],
                equipment=row['equipment'],
                image=row['image']
            )
            db.session.add(recipe)
            db.session.flush()

            # Parse ingredients
            ingredients_list = ast.literal_eval(row['ingredients'])
            for ing in ingredients_list:
                ingredient = Ingredient(name=ing[1], amount=ing[0], recipe_id=recipe.id)
                db.session.add(ingredient)

            # Parse steps
            steps_list = ast.literal_eval(row['steps'])
            for order, step in enumerate(steps_list):
                recipe_step = RecipeStep(step=step, recipe_id=recipe.id, order=order)
                db.session.add(recipe_step)

            db.session.commit()

def main():
    with app.app_context():
        import os
        print(os.getcwd())
        import_csv('allerhande/recipes.csv')

# The following lines should be at the very bottom of the file
if __name__ == "__main__":
    main()
