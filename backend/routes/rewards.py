from flask import Blueprint, request, jsonify
from database import get_db

rewards_bp = Blueprint("rewards", __name__)

# Reward shop catalogue — configurable
REWARD_SHOP = [
    {"id": "badge_eco_starter",   "name": "Eco Starter Badge",    "category": "badge",   "cost": 20,  "rarity": "Common",    "icon": "🌱", "description": "Your first step into the EcoGacha world."},
    {"id": "badge_recycler",      "name": "Recycler Badge",        "category": "badge",   "cost": 40,  "rarity": "Rare",      "icon": "♻️", "description": "Awarded to consistent recyclers."},
    {"id": "badge_ocean_guard",   "name": "Ocean Guardian Badge",  "category": "badge",   "cost": 80,  "rarity": "Epic",      "icon": "🌊", "description": "Fighting marine pollution one scan at a time."},
    {"id": "title_eco_hero",      "name": "Eco Hero Title",        "category": "title",   "cost": 60,  "rarity": "Rare",      "icon": "🦸", "description": "Display this title on your profile."},
    {"id": "title_eco_legend",    "name": "Eco Legend Title",      "category": "title",   "cost": 150, "rarity": "Legendary", "icon": "🌟", "description": "The highest honour in EcoGacha."},
    {"id": "coupon_notebook",     "name": "Free Notebook Coupon",  "category": "coupon",  "cost": 50,  "rarity": "Common",    "icon": "📒", "description": "Redeem at the campus store for a free notebook."},
    {"id": "coupon_tote",         "name": "Tote Bag Coupon",       "category": "coupon",  "cost": 75,  "rarity": "Rare",      "icon": "👜", "description": "Redeem at the campus store for an eco tote bag."},
    {"id": "coupon_merch",        "name": "School Merch Coupon",   "category": "coupon",  "cost": 120, "rarity": "Epic",      "icon": "🎽", "description": "Redeem for official Topfaith University merchandise."},
    {"id": "mystery_crate",       "name": "Mystery Crate",         "category": "crate",   "cost": 50,  "rarity": "Rare",      "icon": "📦", "description": "Open for a random reward — Common to Legendary."},
]


@rewards_bp.route("/shop", methods=["GET"])
def shop():
    return jsonify(REWARD_SHOP), 200


@rewards_bp.route("/redeem", methods=["POST"])
def redeem():
    data = request.get_json()
    student_id = data.get("student_id")
    reward_id  = data.get("reward_id")

    if not student_id or not reward_id:
        return jsonify({"error": "student_id and reward_id are required."}), 400

    reward = next((r for r in REWARD_SHOP if r["id"] == reward_id), None)
    if not reward:
        return jsonify({"error": "Reward not found."}), 404

    cost = reward["cost"]

    conn = get_db()
    student = conn.execute("SELECT tokens FROM students WHERE id = ?", (student_id,)).fetchone()

    if not student:
        conn.close()
        return jsonify({"error": "Student not found."}), 404

    if student["tokens"] < cost:
        conn.close()
        return jsonify({"error": f"Not enough tokens. Need {cost}, you have {student['tokens']}."}), 400

    conn.execute("UPDATE students SET tokens = tokens - ? WHERE id = ?", (cost, student_id))
    conn.execute(
        "INSERT INTO redemptions (student_id, tokens_redeemed, reward_id, reward_name) VALUES (?, ?, ?, ?)",
        (student_id, cost, reward["id"], reward["name"])
    )
    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Successfully redeemed '{reward['name']}' for {cost} EcoTokens!",
        "reward": reward,
        "tokens_spent": cost
    }), 200
