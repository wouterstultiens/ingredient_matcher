import os
import shutil
from app import app
from models import db

def delete_instance_folder(path='instance'):
    if os.path.exists(path):
        shutil.rmtree(path)

def create_directory_for_db(path='instance'):
    if not os.path.exists(path):
        os.makedirs(path)

with app.app_context():
    # Delete the instance folder
    delete_instance_folder()

    # Create the necessary directory for the SQLite database
    create_directory_for_db()
    # Recreate the database
    db.create_all()
    # Import and run the import_recipes script
    from recipe_scraper.import_recipes import main as import_recipes_main
    import_recipes_main()
