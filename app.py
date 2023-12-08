from flask import render_template, request
from config import app, db
from models import Recipe, Ingredient
from flask import jsonify

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ingredients = [i for i in request.form.getlist('ingredient') if i]  # Filter out empty strings
        recipes = Recipe.query.join(Recipe.ingredients).filter(Ingredient.name.in_(ingredients)).group_by(Recipe.id).having(db.func.count(Recipe.id) == len(ingredients)).all()
        return render_template('search_results.html', recipes=recipes, ingredients=ingredients)
    return render_template('search.html')

@app.route('/ingredient-suggestions')
def ingredient_suggestions():
    query = request.args.get('q', '')
    if query:
        ingredient_list = Ingredient.query.with_entities(Ingredient.name).filter(Ingredient.name.startswith(query)).distinct().all()
        suggestions = [ingredient.name for ingredient in ingredient_list]
    else:
        suggestions = []
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)