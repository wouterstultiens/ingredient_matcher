from flask import render_template, request, jsonify
from config import app, db
from models import Recipe, Ingredient


@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('q', '')
    recipes = []
    if query:
        # Check if the query matches an ingredient
        matching_ingredient = Ingredient.query.filter(Ingredient.name.contains(query)).first()
        if matching_ingredient:
            # If it's an ingredient, find all recipes containing it
            recipes = Recipe.query.join(Recipe.ingredients).filter(Ingredient.name.contains(query)).all()
        else:
            # Otherwise, search for recipes by name
            recipes = Recipe.query.filter(Recipe.name.contains(query)).all()

    return render_template('index.html', recipes=recipes, query=query)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if query:
        ingredient_list = Ingredient.query.with_entities(Ingredient.name).filter(
            Ingredient.name.contains(query)).distinct().all()
        recipe_list = Recipe.query.with_entities(Recipe.name).filter(Recipe.name.contains(query)).distinct().all()
        suggestions = [ingredient.name for ingredient in ingredient_list] + [recipe.name for recipe in recipe_list]
        return jsonify(suggestions)
    return jsonify([])


if __name__ == '__main__':
    app.run(debug=True)
