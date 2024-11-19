from flask import Blueprint, request, jsonify

city_bp = Blueprint('city', __name__)

@city_bp.route('/getcities', methods=['GET'])
def get_cities():
    return jsonify({'cities': []})