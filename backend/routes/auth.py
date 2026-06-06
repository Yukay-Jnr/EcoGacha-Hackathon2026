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


@auth_bp.route("/update", methods=["POST"])
def update():
    data = request.get_json()
    student_id = data.get("student_id")
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    new_password = data.get("new_password", "").strip()
    current_password = data.get("current_password", "").strip()

    if not student_id:
        return jsonify({"error": "Not authenticated."}), 401

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()

    if not student:
        conn.close()
        return jsonify({"error": "Student not found."}), 404

    # If changing password, verify current password first
    if new_password:
        if not current_password:
            conn.close()
            return jsonify({"error": "Enter your current password to set a new one."}), 400
        if student["password_hash"] != hash_password(current_password):
            conn.close()
            return jsonify({"error": "Current password is incorrect."}), 401
        if len(new_password) < 6:
            conn.close()
            return jsonify({"error": "New password must be at least 6 characters."}), 400

    # Build update query dynamically
    fields = []
    values = []
    if name:
        fields.append("name = ?")
        values.append(name)
    if email:
        fields.append("email = ?")
        values.append(email)
    if new_password:
        fields.append("password_hash = ?")
        values.append(hash_password(new_password))

    if not fields:
        conn.close()
        return jsonify({"error": "Nothing to update."}), 400

    values.append(student_id)
    try:
        conn.execute(f"UPDATE students SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
    except Exception as e:
        conn.close()
        if "UNIQUE" in str(e):
            return jsonify({"error": "That email is already in use."}), 409
        return jsonify({"error": "Update failed."}), 500

    updated = conn.execute(
        "SELECT id, name, matric_number, email, tokens, total_scans FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()
    conn.close()

    return jsonify({
        "message": "Account updated successfully.",
        "student": dict(updated)
    }), 200
