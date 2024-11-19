from flask import Blueprint, request, jsonify

team_bp = Blueprint('team', __name__)

@team_bp.route('/getteams', methods=['GET'])
def get_teams():
    return jsonify({'teams': []})