from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# Database configuration using environment variables
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'database': os.environ.get('DB_NAME', 'mydb')
}

# Initialize database table
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    routes = {
        'Get all users': '/users [GET]',
        'Get user by id': '/users/<id> [GET]',
        'Create user': '/users [POST]',
        'Update user': '/users/<id> [PUT]',
        'Delete user': '/users/<id> [DELETE]'
    }
    return jsonify(routes)

@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Create database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Execute query
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        # Close connection
        cursor.close()
        conn.close()

        return jsonify(users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ['name', 'email']):
            return jsonify({"error": "Missing required fields"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (data['name'], data['email'])
        )

        conn.commit()
        user_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({"id": user_id, "message": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        update_fields = []
        values = []
        for key in ['name', 'email']:
            if key in data:
                update_fields.append(f"{key} = %s")
                values.append(data[key])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"

        cursor.execute(query, values)
        conn.commit()

        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()

        if affected_rows:
            return jsonify({"message": "User updated successfully"})
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()

        if affected_rows:
            return jsonify({"message": "User deleted successfully"})
        return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True,host='0.0.0.0',port=8080)
