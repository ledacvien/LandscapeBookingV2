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