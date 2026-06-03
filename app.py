import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("app.db")
    return conn

@app.route("/search")
def search():
    # VULNERABILITY: SQL Injection - user input directly in query
    query = request.args.get("q", "")
    db = get_db()
    cursor = db.execute(f"SELECT * FROM users WHERE name = '{query}'")
    results = cursor.fetchall()
    return str(results)

@app.route("/ping")
def ping():
    # VULNERABILITY: Command Injection - user input passed to os.system
    host = request.args.get("host", "localhost")
    os.system(f"ping -c 1 {host}")
    return f"Pinged {host}"

@app.route("/")
def index():
    return "DevSecOps Demo App"

if __name__ == "__main__":
    app.run(debug=True)