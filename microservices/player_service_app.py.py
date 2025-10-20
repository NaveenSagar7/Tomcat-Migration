# === player_service/app.py ===
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'readreplica-1.c7uq2skoqqmb.ap-south-1.rds.amazonaws.com', #readerendpoint
    'user': 'Admin',
    'password': 'Naveensagar30',
    'database': 'realmadrid_db'
}

CLOUDFRONT_URL = "https://d1o92qaptx4j65.cloudfront.net"

@app.route('/players', methods=['GET'])
def get_players():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    for player in players:
        player['image_file'] = f"{CLOUDFRONT_URL}/{player['image_file']}"
    conn.close()
    return jsonify(players)

if __name__ == '__main__':
    app.run(port=5002, host='0.0.0.0')
