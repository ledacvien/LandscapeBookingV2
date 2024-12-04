from flask import Blueprint, request, jsonify
from ..db import get_db_connection

team_bp = Blueprint('team', __name__)

@team_bp.route('/getteams', methods=['GET'])
def get_teams():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM team")
            teams = cur.fetchall()
            return jsonify({'teams': teams})
    return jsonify({'teams': []})

@team_bp.route('/updateteam', methods=['PUT'])
def update_team():
    data = request.json
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE team SET name = %s, address = %s, cityid = %s WHERE teamid = %s",
                (data['name'], data['address'], data['cityid'], data['teamid'])
            )
            conn.commit()
            return jsonify({'message': 'Team updated successfully'}), 200
    return jsonify({'error': 'Failed to update team'}), 400