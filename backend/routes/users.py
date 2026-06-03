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
