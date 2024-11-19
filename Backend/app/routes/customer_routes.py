from flask import Blueprint, request, jsonify

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/getcustomers', methods=['GET'])
def get_customers():
    return jsonify({'customers': []})