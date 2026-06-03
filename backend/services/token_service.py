import random

# ── Categories match exactly what the RISE AI model was trained on ──
# (ImageFolder sorts alphabetically: cardboard, glass, metal, organic, paper, plastic, trash)
CATEGORY_CONFIG = {
    "cardboard": {
        "base_range": (1, 3),
        "reason": "Easily recyclable — great for repulping",
        "decomp": "2–3 months",
        "marine_risk": "Low",
        "disposal": "Paper/Cardboard recycling bin",
        "tip": "Flatten cardboard before recycling — it saves up to 75% more bin space."
    },
    "glass": {
        "base_range": (3, 5),
        "reason": "100% recyclable, reusable indefinitely",
        "decomp": "1,000,000+ years",
        "marine_risk": "Medium",
        "disposal": "Glass recycling bin",
        "tip": "Glass is endlessly recyclable without losing quality. Never put broken glass in general waste."
    },
    "metal": {
        "base_range": (4, 6),
        "reason": "Highly recyclable — saves significant energy",
        "decomp": "50–200 years",
        "marine_risk": "Medium",
        "disposal": "Metal recycling bin",
        "tip": "Recycling one aluminium can saves enough energy to power a TV for 3 hours."
    },
    "organic": {
        "base_range": (1, 2),
        "reason": "Compostable — returns nutrients to the earth",
        "decomp": "Days to weeks",
        "marine_risk": "Low",
        "disposal": "Organic / compost bin",
        "tip": "Composting organic waste significantly reduces methane emissions from landfills."
    },
    "paper": {
        "base_range": (1, 2),
        "reason": "Easily recyclable",
        "decomp": "2–6 weeks",
        "marine_risk": "Low",
        "disposal": "Paper recycling bin",
        "tip": "One tonne of recycled paper saves 17 trees and 26,000 litres of water."
    },
    "plastic": {
        "base_range": (2, 4),
        "reason": "Major marine pollutant — must be recycled",
        "decomp": "~450 years",
        "marine_risk": "Very High",
        "disposal": "Plastic recycling bin",
        "tip": "Rinse plastic bottles before recycling. Plastic is the #1 pollutant in Nigerian waterways."
    },
    "trash": {
        "base_range": (1, 2),
        "reason": "General / non-recyclable waste",
        "decomp": "Varies",
        "marine_risk": "High",
        "disposal": "General waste bin",
        "tip": "Check the EcoDex before binning — many 'trash' items can actually be recycled."
    },
    # Fallback for any unexpected label
    "unknown": {
        "base_range": (1, 1),
        "reason": "Unidentified waste",
        "decomp": "Unknown",
        "marine_risk": "Unknown",
        "disposal": "General waste bin",
        "tip": "When in doubt, separate your waste and check which bin it belongs to."
    }
}

GACHA_TIERS = {
    "Common":    {"weight": 60, "multiplier_range": (1.0, 1.5)},
    "Rare":      {"weight": 30, "multiplier_range": (1.5, 2.5)},
    "Epic":      {"weight": 10, "multiplier_range": (3.0, 5.0)},
}


def calculate_reward(category: str) -> dict:
    category = category.lower()
    config = CATEGORY_CONFIG.get(category, CATEGORY_CONFIG["unknown"])

    base_min, base_max = config["base_range"]
    base_tokens = random.randint(base_min, base_max)

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
