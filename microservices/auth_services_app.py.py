# === auth_service/app.py ===
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'database-1-instance-1.c7uq2skoqqmb.ap-south-1.rds.amazonaws.com', #writerendpoint
    'user': 'Admin',
    'password': 'Naveensagar30',
    'database': 'realmadrid_db'
}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (data['username'], data['password']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Signup successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'message': 'Login successful', 'username': data['username']})
    else:
        return jsonify({'message': 'Login failed'}), 401

if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')
