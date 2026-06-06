# AI Model — Training Notes

## Model
- Architecture: ResNet18 (pretrained on ImageNet, fine-tuned on waste dataset)
- Framework: PyTorch + torchvision
- File: `rise_ai_model.pth`

## What's saved in the .pth file
```python
{
    "model_state_dict": ...,   # ResNet18 weights
    "classes": [...]           # list of class names in training order
}
```

## Categories (sorted alphabetically — matches ImageFolder order)
cardboard, glass, metal, organic, paper, plastic, trash

> Note: The class list is saved inside the .pth file itself.
> labels.txt is a human-readable reference only.

## Image preprocessing (must match training)
- Resize to 224×224
- ToTensor
- Normalize: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]

## How to drop in the model
1. Copy `rise_ai_model.pth` into this `ai_model/` folder
2. Restart the backend (`python app.py`)
3. On startup you should see:
   `EcoGacha AI model loaded. Categories: ['cardboard', 'glass', ...]`

## Demo mode
If the model file is missing, the backend auto-runs in demo mode
with random mock predictions. All other features work normally.

## To retrain
```bash
cd "RISE AI"
python train_model.py
```
Copy the output `rise_ai_model.pth` into `ecogacha/ai_model/`.
