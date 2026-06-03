from flask import Blueprint, request, jsonify
from database import get_db

rewards_bp = Blueprint("rewards", __name__)

MINIMUM_REDEEM = 10


@rewards_bp.route("/redeem", methods=["POST"])
def redeem():
    data = request.get_json()
    student_id = data.get("student_id")
    amount = data.get("amount", 0)

    if not student_id or amount < MINIMUM_REDEEM:
        return jsonify({"error": f"Minimum redemption is {MINIMUM_REDEEM} tokens."}), 400

    conn = get_db()
    student = conn.execute("SELECT tokens FROM students WHERE id = ?", (student_id,)).fetchone()

    if not student:
        return jsonify({"error": "Student not found."}), 404

    if student["tokens"] < amount:
        return jsonify({"error": "Insufficient tokens."}), 400

    conn.execute("UPDATE students SET tokens = tokens - ? WHERE id = ?", (amount, student_id))
    conn.execute("INSERT INTO redemptions (student_id, tokens_redeemed) VALUES (?, ?)", (student_id, amount))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Successfully redeemed {amount} EcoTokens."}), 200
