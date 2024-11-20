from flask import Flask
from flask_cors import CORS
from .routes import register_routes
import os
import psycopg2
from dotenv import load_dotenv
from .db import get_db_connection

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Configuration
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')

    # Register blueprints
    register_routes(app)

    # Test connection to database
    with app.app_context():
        with get_db_connection() as conn:
            print("Connected to database")

    # THis is example branch. You can delete this line
    

    return app