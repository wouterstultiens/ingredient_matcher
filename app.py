from flask import render_template, request
from config import app, db
from models import Recipe

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ingredient = request.form['ingredient']
        # Query the database for recipes containing the ingredient
        recipes = Recipe.query.filter(Recipe.ingredients.like(f'%{ingredient}%')).all()
        return render_template('search_results.html', recipes=recipes, ingredient=ingredient)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)