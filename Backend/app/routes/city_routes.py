from flask import Blueprint, request, jsonify
from ..db import get_db_connection

city_bp = Blueprint('city', __name__)


"""
get_cities()
Fetch all city entries.
[
    {
        "cityid": 1,
        "name": "Tempe",
        "teamid": 1,
        "zip": [85281, 85280, 85281],
        "zipcode": [85282, 85283, 85284]
    },
]
"""

@city_bp.route('/getcities', methods=['GET'])
def get_cities():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM city")
            cities = cur.fetchall()
            return jsonify({'cities': cities}), 200
        

"""
get_city_by_name
Fetch a single city by name
{
  "cityid": 1,
  "name": "Tempe",
  "team_name": "Team1",
  "teamid": 1,
  "zip": [85281, 85280, 85281],
  "zipcode": [85282, 85283, 85284]
}
"""
@city_bp.route('/name/<string:cityname>', methods=['GET'])
def get_city_by_name(cityname):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                print(f"Searching for city: {cityname}")  # Debug print
                
                # Query to get city and its associated team information
                query = """
                    SELECT c.cityid, c.name, c.teamid, c.zip, c.zipcode, t.name as team_name
                    FROM city c
                    LEFT JOIN team t ON c.teamid = t.teamid
                    WHERE LOWER(c.name) = LOWER(%s)
                """
                print(f"Executing query: {query}")  # Debug print
                print(f"With parameter: {cityname}")  # Debug print
                
                cur.execute(query, (cityname,))
                
                result = cur.fetchone()
                print(f"Query result: {result}")  # Debug print
                
                if result:
                    response = {
                        'cityid': result['cityid'],
                        'name': result['name'],
                        'teamid': result['teamid'],
                        'zip': result['zip'],
                        'zipcode': result['zipcode'],
                        'team_name': result['team_name']
                    }
                    print(f"Returning response: {response}")  # Debug print
                    return jsonify(response), 200
                else:
                    return jsonify({'error': 'City not found'}), 404
                    
            except Exception as e:
                print(f"Detailed error information: {str(e)}")  # More detailed error print
                print(f"Error type: {type(e)}")  # Print error type
                return jsonify({'error': f'Database error: {str(e)}'}), 500
"""
add_city()
Add city entry.
[
   {
    "message": "City added successfully",
    "city": {
        "cityid": 5,
        "name": "Phoenix",
        "teamid": 5,
        "zip": [85001, 85002, 85003],
        "zipcode": [85004, 85005, 85006]
        }
    }
]
"""

@city_bp.route('/addcity', methods=['POST'])
def add_city():
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'teamid', 'zip', 'zipcode']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                # Start transaction
                cur.execute("BEGIN")
                
                # Check if team exists and isn't already assigned to a city
                cur.execute("""
                    SELECT 1 FROM team 
                    WHERE teamid = %s AND cityid IS NULL
                """, (data['teamid'],))
                if not cur.fetchone():
                    return jsonify({'error': 'Team does not exist or is already assigned to a city'}), 400
                
                # Check if city name already exists
                cur.execute("SELECT 1 FROM city WHERE name = %s", (data['name'],))
                if cur.fetchone():
                    return jsonify({'error': 'City already exists'}), 400
                
                # Add city
                cur.execute("""
                    INSERT INTO city (name, teamid, zip, zipcode)
                    VALUES (%s, %s, %s, %s)
                    RETURNING cityid, name, teamid, zip, zipcode
                """, (
                    data['name'],
                    data['teamid'],
                    data['zip'],
                    data['zipcode']
                ))
                
                new_city_data = cur.fetchone()
                
                # Update the team with the new cityid
                cur.execute("""
                    UPDATE team 
                    SET cityid = %s 
                    WHERE teamid = %s
                """, (new_city_data[0], data['teamid']))
                
                # Update any existing customer records with this city name
                cur.execute("""
                    UPDATE customer 
                    SET city = %s 
                    WHERE city = %s
                """, (data['name'], data['name']))
                
                # Commit transaction
                cur.execute("COMMIT")
                
                # Return complete city information
                return jsonify({
                    'message': 'City added successfully',
                    'city': {
                        'cityid': new_city_data['cityid'],
                        'name': new_city_data['name'],
                        'teamid': new_city_data['teamid'],
                        'zip': new_city_data['zip'],
                        'zipcode': new_city_data['zipcode']
                    }
                }), 201
                
            except Exception as e:
                cur.execute("ROLLBACK")
                print(f"Error adding city: {str(e)}")
                return jsonify({'error': 'Failed to add city. Database error'}), 400    





