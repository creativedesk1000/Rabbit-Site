from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb

app = Flask(__name__)
CORS(app)

# Database Connection
db = MySQLdb.connect(
    host="localhost",
    user="root",          # apna MySQL username
    passwd="",            # MySQL password agar hai to yahan likho
    db="labmid"
)
cursor = db.cursor()

@app.route("/")
def home():
    return "Backend running..."

# Signup API
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (name, email, password))
        db.commit()
        return jsonify({"message": "Signup successful"}), 201
    except:
        return jsonify({"message": "Email already exists"}), 400

# Login API
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)
