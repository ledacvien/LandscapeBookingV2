from flask import Flask
from .routes import register_routes
import os
import psycopg2
from dotenv import load_dotenv
from .db import get_db_connection

load_dotenv()

def create_app():
    app = Flask(__name__)
    # Configuration
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')

    # Register blueprints
    register_routes(app)

    # Test connection to database
    with app.app_context():
        with get_db_connection() as conn:
            print("Connected to database")
    

    return app