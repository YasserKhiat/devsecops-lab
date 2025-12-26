from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os

app = Flask(__name__)

# Load secret key from environment variable (safer than hardcoding)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-placeholder")


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    # Use parameterized queries to prevent SQL injection
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"status": "success", "user": username})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")
    # Simple validation to prevent command injection
    if not host.replace(".", "").replace("-", "").isalnum():
        return jsonify({"error": "Invalid host"}), 400

    import platform
    import subprocess

    ping_cmd = ["ping", "-c", "1", host] if platform.system() != "Windows" else ["ping", "-n", "1", host]
    try:
        output = subprocess.check_output(ping_cmd, stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output}), 400


@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "")
    # Avoid eval() — allow only safe arithmetic expressions
    import re
    if not re.match(r"^[0-9+\-*/().\s]+$", expression):
        return jsonify({"error": "Invalid expression"}), 400
    try:
        result = eval(expression, {"__builtins__": {}})
        return jsonify({"result": result})
    except Exception:
        return jsonify({"error": "Error computing expression"}), 400


@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "")
    if not pwd:
        return jsonify({"error": "Password required"}), 400
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    return jsonify({"bcrypt": hashed})


@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename", "")
    # Prevent directory traversal attacks
    if ".." in filename or filename.startswith("/"):
        return jsonify({"error": "Invalid filename"}), 400

    try:
        with open(os.path.join("files", filename), "r") as f:
            content = f.read()
        return jsonify({"content": content})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@app.route("/debug", methods=["GET"])
def debug():
    # Remove exposing secrets in production
    return jsonify({"debug": False})


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Welcome to the secure DevSecOps API"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
