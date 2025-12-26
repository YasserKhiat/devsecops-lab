# api/app.py [cite: 58-112]
from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os

app = Flask(__name__)
SECRET_KEY = "dev-secret-key-12345"  # Secret codé en dur (Mauvaise pratique)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Injection SQL possible ici
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": username}
    return {"status": "error", "message": "Invalid credentials"}

@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "1+1")
    result = eval(expression)  # faille critique : exécution de code arbitraire
    return {"result": result}

@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "admin")
    # Utilisation de MD5 (algorithme faible)
    hashed = hashlib.md5(pwd.encode()).hexdigest()
    return {"md5": hashed}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)