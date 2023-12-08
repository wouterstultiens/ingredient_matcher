from flask import render_template, request
from config import app, db
from models import Recipe, Ingredient

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ingredients = request.form.getlist('ingredient')
        # Query for recipes containing all ingredients
        recipes = Recipe.query.join(Recipe.ingredients).filter(Ingredient.name.in_(ingredients)).group_by(Recipe.id).having(db.func.count(Recipe.id) == len(ingredients)).all()
        return render_template('search_results.html', recipes=recipes, ingredients=ingredients)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)