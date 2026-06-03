from flask import Blueprint, request, jsonify
from database import get_db
from services.ai_service import classify_image
from services.token_service import calculate_reward

scan_bp = Blueprint("scan", __name__)


@scan_bp.route("/classify", methods=["POST"])
def classify():
    student_id = request.form.get("student_id")
    if not student_id:
        return jsonify({"error": "student_id is required."}), 400

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()

    # Classify the image
    classification = classify_image(image_bytes)
    category = classification["category"]
    confidence = classification["confidence"]

    # Calculate gacha reward
    reward = calculate_reward(category)
    tokens = reward["tokens_earned"]

    # Save to DB
    conn = get_db()
    try:
        conn.execute(
            """INSERT INTO scans (student_id, waste_category, confidence, tokens_earned, gacha_tier, eco_tip)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (student_id, category, confidence, tokens, reward["gacha_tier"], reward["eco_tip"])
        )
        conn.execute(
            "UPDATE students SET tokens = tokens + ?, total_scans = total_scans + 1 WHERE id = ?",
            (tokens, student_id)
        )
        conn.commit()
    finally:
        conn.close()

    return jsonify({
        "category": category,
        "confidence": confidence,
        "tokens_earned": tokens,
        "gacha_tier": reward["gacha_tier"],
        "eco_tip": reward["eco_tip"],
        "disposal": reward["disposal"],
        "decomp": reward["decomp"],
        "marine_risk": reward["marine_risk"],
        "demo_mode": classification.get("demo_mode", False)
    }), 200
