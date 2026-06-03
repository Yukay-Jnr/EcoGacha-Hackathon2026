from flask import Blueprint, request, jsonify
from database import get_db
import hashlib
import re

auth_bp = Blueprint("auth", __name__)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name", "").strip()
    matric = data.get("matric_number", "").strip().upper()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not all([name, matric, email, password]):
        return jsonify({"error": "All fields are required."}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO students (name, matric_number, email, password_hash) VALUES (?, ?, ?, ?)",
            (name, matric, email, hash_password(password))
        )
        conn.commit()
        return jsonify({"message": "Account created successfully."}), 201
    except Exception as e:
        if "UNIQUE" in str(e):
            return jsonify({"error": "Matric number or email already registered."}), 409
        return jsonify({"error": "Registration failed."}), 500
    finally:
        conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    matric = data.get("matric_number", "").strip().upper()
    password = data.get("password", "")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE matric_number = ? AND password_hash = ?",
        (matric, hash_password(password))
    ).fetchone()
    conn.close()

    if not student:
        return jsonify({"error": "Invalid matric number or password."}), 401

    return jsonify({
        "message": "Login successful.",
        "student": {
            "id": student["id"],
            "name": student["name"],
            "matric_number": student["matric_number"],
            "email": student["email"],
            "tokens": student["tokens"],
            "total_scans": student["total_scans"]
        }
    }), 200
