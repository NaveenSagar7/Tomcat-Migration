# === frontend/app.py ===
from flask import Flask, render_template_string, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'super-secret-key'

AUTH_SERVICE_URL = "http://localhost:5001"
PLAYER_SERVICE_URL = "http://localhost:5002"

@app.route('/')
def home():
    return render_template_string('''
        <html>
        <head>
            <title>Welcome</title>
            <style>
                body { background-color: orange; text-align: center; }
                .form-box { background: white; color: black; padding: 20px; border-radius: 10px; margin: auto; width: 300px; }
            </style>
        </head>
        <body>
            <h1>Welcome to RealMadrid</h1>
            <div class="form-box">
                <h3>Signup</h3>
                <form method="POST" action="/signup">
                    Username: <input name="username" required><br><br>
                    Password: <input name="password" type="password" required><br><br>
                    <button type="submit">Signup</button>
                </form>
            </div>

            <div class="form-box">
                <h3>Login</h3>
                <form method="POST" action="/login">
                    Username: <input name="username" required><br><br>
                    Password: <input name="password" type="password" required><br><br>
                    <button type="submit">Login</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    res = requests.post(f"{AUTH_SERVICE_URL}/signup", json={'username': username, 'password': password})
    if res.status_code == 200:
        session['username'] = username
        return redirect('/dashboard')
    return "Signup failed"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    res = requests.post(f"{AUTH_SERVICE_URL}/login", json={'username': username, 'password': password})
    if res.status_code == 200:
        session['username'] = username
        return redirect('/dashboard')
    return "Login failed"

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    res = requests.get(f"{PLAYER_SERVICE_URL}/players")
    players = res.json()
    return render_template_string('''
        <html>
        <head><title>Dashboard</title></head>
        <body>
            <h2>Welcome to RealMadrid Fan App!</h2>
            <h3>Player Gallery:</h3>
            {% for player in players %}
                <div>
                    <strong>{{ player.player_name }}</strong><br>
                    <img src="{{ player.image_file }}" width="200"><br><br>
                </div>
            {% endfor %}
        </body>
        </html>
    ''', players=players)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
