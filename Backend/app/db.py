import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

def get_db_connection():
    try:
        conn = psycopg2.connect(
            current_app.config['DATABASE_URL'], 
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise e
    