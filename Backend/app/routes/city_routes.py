from flask import Blueprint, request, jsonify
from ..db import get_db_connection

city_bp = Blueprint('city', __name__)

@city_bp.route('/getcities', methods=['GET'])
def get_orders():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM city")
            cities = cur.fetchall()
            return jsonify({'cities': cities})
