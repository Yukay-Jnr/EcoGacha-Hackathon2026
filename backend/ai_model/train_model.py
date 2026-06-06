import torch
import torch.nn as nn
import torch.optim as optim

from collections import Counter
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, Subset

dataset_path = "dataset-resized"
batch_size = 32
epochs = 30
learning_rate = 0.001
validation_fraction = 0.2
random_seed = 42
model_path = "rise_ai_model.pth"

# Define transformations for the training and validation sets.
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load the dataset
base_dataset = datasets.ImageFolder(root=dataset_path)
train_base_dataset = datasets.ImageFolder(root=dataset_path, transform=train_transform)
val_base_dataset = datasets.ImageFolder(root=dataset_path, transform=val_transform)

print(f"Total dataset size: {len(base_dataset)}")
print(f"Classes: {base_dataset.classes}")

if len(base_dataset.classes) < 2:
    raise ValueError(
        f"Expected at least 2 classes, but found {len(base_dataset.classes)}: {base_dataset.classes}. "
        "Check that dataset_path points to the folder containing the class subfolders."
    )

# Split the dataset into stratified training and validation sets.
generator = torch.Generator().manual_seed(random_seed)
targets = torch.tensor(base_dataset.targets)
train_indices, val_indices = [], []

for class_index in range(len(base_dataset.classes)):
    class_indices = torch.where(targets == class_index)[0]
    shuffled_indices = class_indices[torch.randperm(len(class_indices), generator=generator)]
    val_count = max(1, int(round(len(shuffled_indices) * validation_fraction)))

    val_indices.extend(shuffled_indices[:val_count].tolist())
    train_indices.extend(shuffled_indices[val_count:].tolist())

train_dataset = Subset(train_base_dataset, train_indices)
val_dataset = Subset(val_base_dataset, val_indices)

def class_counts(indices):
    counts = Counter(base_dataset.targets[index] for index in indices)
    return {
        base_dataset.classes[class_index]: counts[class_index]
        for class_index in range(len(base_dataset.classes))
    }

print(f"Training set size: {len(train_dataset)}")
print(f"Validation set size: {len(val_dataset)}")
print(f"Training class counts: {class_counts(train_indices)}")
print(f"Validation class counts: {class_counts(val_indices)}")

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load a pre-trained ResNet model and modify the final layer
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(base_dataset.classes))
model = model.to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
best_accuracy = -1.0

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f"Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss:.4f}")

    # Validation loop
    model.eval()
    correct, total = 0, 0
    validation_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            validation_loss += loss.item() * images.size(0)
            predicted = outputs.argmax(1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    validation_loss = validation_loss / len(val_loader.dataset)
    print(f"Validation Loss: {validation_loss:.4f}, Validation Accuracy: {accuracy:.4f}")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "classes": base_dataset.classes
            },
            model_path
        )
        print(f"Saved new best model to '{model_path}'")

print(f"Model training complete. Best validation accuracy: {best_accuracy:.4f}")
