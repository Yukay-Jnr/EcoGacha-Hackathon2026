from flask import Blueprint, request, jsonify
from database import get_db

users_bp = Blueprint("users", __name__)


@users_bp.route("/<int:student_id>/balance", methods=["GET"])
def balance(student_id):
    conn = get_db()
    student = conn.execute(
        "SELECT name, matric_number, tokens, total_scans FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()
    conn.close()

    if not student:
        return jsonify({"error": "Student not found."}), 404

    return jsonify(dict(student)), 200


@users_bp.route("/<int:student_id>/history", methods=["GET"])
def history(student_id):
    conn = get_db()
    scans = conn.execute(
        """SELECT waste_category, confidence, tokens_earned, gacha_tier, eco_tip, scanned_at
           FROM scans WHERE student_id = ? ORDER BY scanned_at DESC LIMIT 20""",
        (student_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(s) for s in scans]), 200


@users_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn = get_db()
    rows = conn.execute(
        "SELECT name, matric_number, tokens, total_scans FROM students ORDER BY tokens DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200


@users_bp.route("/<int:student_id>/update", methods=["POST"])
def update(student_id):
    import hashlib
    data = request.get_json()
    conn = get_db()

    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return jsonify({"error": "Student not found."}), 404

    name     = data.get("name", "").strip() or student["name"]
    email    = data.get("email", "").strip() or student["email"]
    password = data.get("password", "").strip()

    if password:
        if len(password) < 6:
            conn.close()
            return jsonify({"error": "Password must be at least 6 characters."}), 400
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
    else:
        pw_hash = student["password_hash"]

    try:
        conn.execute(
            "UPDATE students SET name = ?, email = ?, password_hash = ? WHERE id = ?",
            (name, email, pw_hash, student_id)
        )
        conn.commit()
        updated = conn.execute("SELECT id, name, matric_number, email, tokens, total_scans FROM students WHERE id = ?", (student_id,)).fetchone()
        conn.close()
        return jsonify({"message": "Account updated successfully.", "student": dict(updated)}), 200
    except Exception as e:
        conn.close()
        if "UNIQUE" in str(e):
            return jsonify({"error": "That email is already used by another account."}), 409
        return jsonify({"error": "Update failed."}), 500
