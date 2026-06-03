import argparse
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


MODEL_PATH = "rise_ai_model.pth"


def load_model(model_path):
    checkpoint = torch.load(model_path, map_location="cpu")
    classes = checkpoint["classes"]

    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, len(classes))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    return model, classes


def predict_image(model, image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)[0]

    return probabilities


def main():
    parser = argparse.ArgumentParser(description="Predict the class of a trash image.")
    parser.add_argument("image", help="Path to the image to classify.")
    parser.add_argument(
        "--model",
        default=MODEL_PATH,
        help=f"Path to the trained model checkpoint. Default: {MODEL_PATH}"
    )
    args = parser.parse_args()

    image_path = Path(args.image)
    model_path = Path(args.model)

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    model, classes = load_model(model_path)
    probabilities = predict_image(model, image_path)
    predicted_index = probabilities.argmax().item()

    print(f"Prediction: {classes[predicted_index]}")
    print(f"Confidence: {probabilities[predicted_index].item():.4f}")
    print("Class probabilities:")

    for class_name, probability in sorted(
        zip(classes, probabilities.tolist()),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"  {class_name}: {probability:.4f}")


if __name__ == "__main__":
    main()
