from flask import render_template, request, jsonify
from config import app, db
from models import Recipe, Ingredient


@app.route('/', methods=['GET'])
def index():
    min_rating = request.args.get('minRating', 0.5, type=float)
    min_rating_count = request.args.get('minRatingCount', 0, type=int)
    sort_option = request.args.get('sortOption', 'name')

    # Modify query based on filters and sorting
    query = Recipe.query
    if min_rating:
        query = query.filter(Recipe.rating >= min_rating)
    if min_rating_count:
        query = query.filter(Recipe.rating_count >= min_rating_count)
    if sort_option == 'rating':
        query = query.order_by(Recipe.rating.desc(), Recipe.name)
    else:
        query = query.order_by(Recipe.name)

    recipes = query.all()
    return render_template('index.html', recipes=recipes)


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

@app.route('/recipe-page', methods=['GET'])
def recipe_page():
    recipe_id = request.args.get('recipe', '')
    if recipe_id:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            return render_template('recipe_page.html', recipe=recipe)
    return render_template('404.html')  # Template for page not found


if __name__ == '__main__':
    app.run(debug=True)
