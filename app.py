from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# Establish database connection
db = mysql.connector.connect(**db_config)

# GET /api/candy - Retrieve all candies using the GetCandies procedure
@app.route('/api/candy', methods=['GET'])
def get_candies():
    cursor = db.cursor()
    cursor.callproc("GetCandies")
    results = cursor.fetchall()
    cursor.close()
    candies = []

    for row in results:
        candy_id, candy_name, image_url, description = row
        candy = {
            'id': candy_id,
            'name': candy_name,
            'image_url': image_url,
            'description': description
        }
        candies.append(candy)

    return jsonify(candies)

# POST /api/candy - Create a new candy using the CreateCandy procedure
@app.route('/api/candy', methods=['POST'])
def create_candy():
    name = request.json['name']
    image_url = request.json['image_url']
    description = request.json['description']

    cursor = db.cursor()
    cursor.callproc("CreateCandy", (name, image_url, description))
    results = cursor.fetchone()
    cursor.close()

    new_candy_id = results[0]
    new_candy = {
        'id': new_candy_id,
        'name': name,
        'image_url': image_url,
        'description': description
    }

    return jsonify(new_candy), 201

# DELETE /api/candy - Delete a candy using the DeleteCandy procedure
@app.route('/api/candy', methods=['DELETE'])
def delete_candy():
    candy_id = request.args.get('id')

    cursor = db.cursor()
    cursor.callproc("DeleteCandy", (candy_id,))
    results = cursor.fetchone()
    cursor.close()

    num_rows_deleted = results[0]

    if num_rows_deleted > 0:
        return jsonify({'message': f"Candy with ID {candy_id} deleted."})
    else:
        return jsonify({'message': f"Candy with ID {candy_id} not found."}), 404

if __name__ == '__main__':
    app.run()
