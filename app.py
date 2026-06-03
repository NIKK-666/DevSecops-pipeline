import subprocess
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
    # FIXED: Using subprocess.run with list arguments instead of os.system
    host = request.args.get("host", "localhost")
    result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
    return f"Pinged {host}: {result.stdout}"

@app.route("/")
def index():
    return "DevSecOps Demo App"

if __name__ == "__main__":
    app.run(debug=True)