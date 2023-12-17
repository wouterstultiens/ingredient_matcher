from flask import Blueprint, render_template, request, jsonify
from models import Recipe, Ingredient

# Blueprint setup
main = Blueprint('main', __name__)

# Home route
@main.route('/', methods=['GET'])
def index():
    min_rating = request.args.get('minRating', 0.5, type=float)
    min_rating_count = request.args.get('minRatingCount', 0, type=int)
    sort_option = request.args.get('sortOption', 'name')
    query_param = request.args.get('query', '')
    recipes = fetch_recipes(min_rating, min_rating_count, sort_option, query_param)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('partials/recipe_grid.html', recipes=recipes)
    return render_template('index.html', recipes=recipes)

# Search route
@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    suggestions = fetch_suggestions(query) if query else []
    return jsonify(suggestions)

# Individual recipe page route
@main.route('/recipe-page', methods=['GET'])
def recipe_page():
    recipe_id = request.args.get('recipe', '')
    recipe = Recipe.query.get(recipe_id) if recipe_id else None
    return render_template('recipe_page.html', recipe=recipe) if recipe else render_template('404.html')

# Helper function to fetch recipes based on search criteria
def fetch_recipes(min_rating, min_rating_count, sort_option, query_param):
    query = Recipe.query
    if min_rating:
        query = query.filter(Recipe.rating >= min_rating)
    if min_rating_count:
        query = query.filter(Recipe.rating_count >= min_rating_count)
    if sort_option == 'rating':
        query = query.order_by(Recipe.rating.desc(), Recipe.name)
    else:
        query = query.order_by(Recipe.name)
    if query_param:
        query = query.filter(Recipe.name.contains(query_param) |
                             Recipe.ingredients.any(Ingredient.name.contains(query_param)))
    return query.all()

# Helper function to fetch search suggestions
def fetch_suggestions(query):
    ingredient_list = Ingredient.query.with_entities(Ingredient.name).filter(
        Ingredient.name.contains(query)).distinct().all()
    recipe_list = Recipe.query.with_entities(Recipe.name).filter(Recipe.name.contains(query)).distinct().all()
    return [ingredient.name for ingredient in ingredient_list] + [recipe.name for recipe in recipe_list]
