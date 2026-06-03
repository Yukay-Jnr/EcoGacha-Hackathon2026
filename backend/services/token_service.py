import random

# Base token ranges per waste category
CATEGORY_CONFIG = {
    "e-waste": {
        "base_range": (10, 15),
        "reason": "Hazardous materials — needs careful disposal",
        "decomp": "Varies (100s of years for components)",
        "marine_risk": "High",
        "disposal": "E-Waste recycling centre",
        "tip": "Never throw electronics in general waste. They contain toxic metals that leach into soil and water."
    },
    "battery": {
        "base_range": (8, 12),
        "reason": "Toxic chemicals — high hazard",
        "decomp": "100+ years",
        "marine_risk": "Very High",
        "disposal": "Hazardous waste bin",
        "tip": "Batteries contain lead, mercury, and cadmium. A single battery can contaminate 600,000 litres of water."
    },
    "metal": {
        "base_range": (4, 6),
        "reason": "Highly recyclable — saves significant energy",
        "decomp": "50–200 years",
        "marine_risk": "Medium",
        "disposal": "Metal recycling bin",
        "tip": "Recycling one aluminium can saves enough energy to power a TV for 3 hours."
    },
    "glass": {
        "base_range": (3, 5),
        "reason": "Reusable but hazardous if broken",
        "decomp": "1,000,000+ years",
        "marine_risk": "Medium",
        "disposal": "Glass recycling bin",
        "tip": "Glass is 100% recyclable and can be recycled endlessly without losing quality."
    },
    "plastic": {
        "base_range": (2, 4),
        "reason": "Major marine pollutant",
        "decomp": "~450 years",
        "marine_risk": "Very High",
        "disposal": "Plastic recycling bin",
        "tip": "Rinse plastic bottles before recycling. Plastic is the #1 pollutant in Nigerian waterways."
    },
    "cardboard": {
        "base_range": (1, 3),
        "reason": "Easily recyclable paper product",
        "decomp": "2–3 months",
        "marine_risk": "Low",
        "disposal": "Paper/cardboard bin",
        "tip": "Flatten cardboard boxes before recycling — it saves up to 75% more bin space."
    },
    "paper": {
        "base_range": (1, 2),
        "reason": "Easily recyclable",
        "decomp": "2–6 weeks",
        "marine_risk": "Low",
        "disposal": "Paper recycling bin",
        "tip": "One tonne of recycled paper saves 17 trees and 26,000 litres of water."
    },
    "organic": {
        "base_range": (1, 2),
        "reason": "Compostable — returns to the earth",
        "decomp": "Days to weeks",
        "marine_risk": "Low",
        "disposal": "Organic/compost bin",
        "tip": "Composting organic waste reduces methane emissions from landfills significantly."
    },
    "unknown": {
        "base_range": (1, 2),
        "reason": "Unidentified waste",
        "decomp": "Unknown",
        "marine_risk": "Unknown",
        "disposal": "General waste bin",
        "tip": "When in doubt, check the EcoDex to learn how to sort your waste properly."
    }
}

# Gacha tier probabilities
GACHA_TIERS = {
    "Common":    {"weight": 60, "multiplier_range": (1.0, 1.5)},
    "Rare":      {"weight": 30, "multiplier_range": (1.5, 2.5)},
    "Epic":      {"weight": 10, "multiplier_range": (3.0, 5.0)},
}


def calculate_reward(category: str) -> dict:
    """
    Given a waste category, runs the gacha roll and returns reward info.
    """
    category = category.lower()
    config = CATEGORY_CONFIG.get(category, CATEGORY_CONFIG["unknown"])

    base_min, base_max = config["base_range"]
    base_tokens = random.randint(base_min, base_max)

    # Weighted gacha roll
    tiers = list(GACHA_TIERS.keys())
    weights = [GACHA_TIERS[t]["weight"] for t in tiers]
    tier = random.choices(tiers, weights=weights, k=1)[0]

    mult_min, mult_max = GACHA_TIERS[tier]["multiplier_range"]
    multiplier = round(random.uniform(mult_min, mult_max), 2)
    final_tokens = max(1, round(base_tokens * multiplier))

    return {
        "tokens_earned": final_tokens,
        "gacha_tier": tier,
        "base_tokens": base_tokens,
        "multiplier": multiplier,
        "reason": config["reason"],
        "decomp": config["decomp"],
        "marine_risk": config["marine_risk"],
        "disposal": config["disposal"],
        "eco_tip": config["tip"]
    }


def get_category_info(category: str) -> dict:
    category = category.lower()
    return CATEGORY_CONFIG.get(category, CATEGORY_CONFIG["unknown"])
