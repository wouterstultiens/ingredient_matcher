from flask import render_template, request, jsonify
from config import app, db
from models import Recipe, Ingredient

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q', '')
    if query:
        ingredient_list = Ingredient.query.with_entities(Ingredient.name).filter(Ingredient.name.contains(query)).distinct().all()
        recipe_list = Recipe.query.with_entities(Recipe.name).filter(Recipe.name.contains(query)).distinct().all()
        suggestions = [ingredient.name for ingredient in ingredient_list] + [recipe.name for recipe in recipe_list]
        return jsonify(suggestions)
    return render_template('index.html')

@app.route('/search-results')
def search_results():
    query = request.args.get('q', '')
    if query:
        # Check if the query matches an ingredient
        matching_ingredient = Ingredient.query.filter(Ingredient.name.contains(query)).first()
        if matching_ingredient:
            # If it's an ingredient, find all recipes containing it
            recipes = Recipe.query.join(Recipe.ingredients).filter(Ingredient.name.contains(query)).all()
        else:
            # Otherwise, search for recipes by name
            recipes = Recipe.query.filter(Recipe.name.contains(query)).all()

        return render_template('search_results.html', recipes=recipes, query=query)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
