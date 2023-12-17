from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from config import Config
from models import db
from routes.main import main

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_and_initialize_db(app):
    with app.app_context():
        # Check if the database exists, if not, create it
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
            print("Database created and initialized.")

        # Check if the database is empty (no recipes)
        from models import Recipe
        if not Recipe.query.first():
            # If empty, import recipes
            from recipe_scraper.import_recipes import main as import_recipes_main
            import_recipes_main()
            print("Recipes imported.")

app.register_blueprint(main)

if __name__ == '__main__':
    create_and_initialize_db(app)
    app.run(debug=True)
