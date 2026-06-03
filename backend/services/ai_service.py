import os
import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ai_model", "rise_ai_model.pth")

# ImageNet normalisation — must match what was used during training
TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

model = None
labels = []


def load_model():
    global model, labels
    try:
        checkpoint = torch.load(MODEL_PATH, map_location="cpu")
        labels = checkpoint["classes"]           # list of class names saved during training

        net = models.resnet18(weights=None)
        net.fc = nn.Linear(net.fc.in_features, len(labels))
        net.load_state_dict(checkpoint["model_state_dict"])
        net.eval()

        model = net
        print(f"EcoGacha AI model loaded. Categories: {labels}")
    except FileNotFoundError:
        print("Warning: rise_ai_model.pth not found — running in demo mode.")
    except Exception as e:
        print(f"Warning: Model failed to load ({e}) — running in demo mode.")


def classify_image(image_bytes: bytes) -> dict:
    """
    Takes raw image bytes, returns classification result dict.
    Falls back to mock predictions if model is not loaded.
    """
    if model is None:
        return _mock_classify()

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = TRANSFORM(img).unsqueeze(0)       # shape: [1, 3, 224, 224]

        with torch.no_grad():
            outputs = model(tensor)
            probs = torch.softmax(outputs, dim=1)[0]

        idx = int(probs.argmax().item())
        confidence = round(float(probs[idx].item()) * 100, 2)
        category = labels[idx]

        return {
            "category": category,
            "confidence": confidence,
            "all_scores": {
                labels[i]: round(float(probs[i].item()) * 100, 2)
                for i in range(len(labels))
            }
        }
    except Exception as e:
        print(f"Classification error: {e}")
        return _mock_classify()


def _mock_classify() -> dict:
    """Demo mode — random predictions for testing without a model file."""
    import random
    cats = ["cardboard", "glass", "metal", "organic", "paper", "plastic", "trash"]
    cat = random.choice(cats)
    conf = round(random.uniform(72, 97), 2)
    return {
        "category": cat,
        "confidence": conf,
        "all_scores": {c: round(random.uniform(0, 100), 2) for c in cats},
        "demo_mode": True
    }
