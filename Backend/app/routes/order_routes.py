from flask import Blueprint, request, jsonify
from ..db import get_db_connection

order_bp = Blueprint('order', __name__)

@order_bp.route('/getorders', methods=['GET'])
def get_orders():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM orders")
            orders = cur.fetchall()
            return jsonify({'orders': orders})
    return jsonify({'orders': []})