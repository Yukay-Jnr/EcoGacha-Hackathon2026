# RISE AI Trash Image Classifier

This project trains a PyTorch image classifier to recognize trash categories from local images. It uses a pretrained ResNet18 model and fine-tunes it on the dataset in `dataset-resized`.

The model predicts one of these classes:

- `cardboard`
- `glass`
- `metal`
- `paper`
- `plastic`
- `trash`

## Project Files

```text
RISE AI/
+-- dataset-resized/
|   +-- cardboard/
|   +-- glass/
|   +-- metal/
|   +-- paper/
|   +-- plastic/
|   +-- trash/
+-- predict.py
+-- requirements.txt
+-- rise_ai_model.pth
+-- train_model.py
```

## Dataset

The training script uses `torchvision.datasets.ImageFolder`, so the dataset must be arranged with one folder per class:

```text
dataset-resized/
+-- cardboard/
+-- glass/
+-- metal/
+-- paper/
+-- plastic/
+-- trash/
```

Each image inside a class folder gets that folder's label.

Current dataset size:

```text
Total images: 2527
Classes: 6
```

Class counts:

```text
cardboard: 403
glass: 501
metal: 410
paper: 594
plastic: 482
trash: 137
```

## Setup

Create and activate your virtual environment if needed:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Training

Run:

```powershell
python train_model.py
```

The training script:

- Loads images from `dataset-resized`
- Confirms that at least 2 classes exist
- Uses a reproducible random seed
- Splits the dataset into training and validation sets
- Keeps the split stratified so each class appears in validation
- Uses train-only augmentation
- Uses clean validation transforms
- Fine-tunes a pretrained ResNet18 model
- Saves the best validation model to `rise_ai_model.pth`

Important training settings:

```python
batch_size = 32
epochs = 30
learning_rate = 0.001
validation_fraction = 0.2
random_seed = 42
model_path = "rise_ai_model.pth"
```

## Training Output

During training, you will see output like:

```text
Total dataset size: 2527
Classes: ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
Training set size: ...
Validation set size: ...
Using device: cpu
Epoch [1/30], Loss: ...
Validation Loss: ..., Validation Accuracy: ...
Saved new best model to 'rise_ai_model.pth'
```

If CUDA is available, the script uses GPU automatically:

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

## Validation Accuracy Notes

Earlier, validation accuracy showed `1.0000` because the dataset path pointed one folder too high. `ImageFolder` was seeing only one class, so every validation image had the same label.

The correct dataset path is now:

```python
dataset_path = "dataset-resized"
```

This works because `dataset-resized` directly contains the class folders.

A validation accuracy of `1.0000` can still happen, but it should be treated carefully. If it happens again, check for:

- Duplicate images across classes
- Very similar images in both training and validation
- A validation set that is too easy
- Images accidentally placed in the wrong folders
- Testing on images from the same dataset instead of new real-world images

## Validation Loss and Accuracy

It is normal for validation loss and validation accuracy to move up and down between epochs.

Good pattern:

```text
Training loss generally decreases
Validation loss generally decreases or stays stable
Validation accuracy generally increases or stays stable
```

Warning pattern:

```text
Training loss keeps decreasing
Validation loss keeps increasing
Validation accuracy stops improving or drops
```

That usually means the model is overfitting.

The script saves the best model based on validation accuracy, so small ups and downs are okay.

## Prediction

After training, use `predict.py` to classify an image.

Basic usage:

```powershell
python predict.py path\to\image.jpg
```

Example:

```powershell
python predict.py dataset-resized\glass\glass1.jpg
```

The script outputs:

```text
Prediction: glass
Confidence: 0.9234
Class probabilities:
  glass: 0.9234
  plastic: 0.0412
  metal: 0.0185
  paper: 0.0101
  cardboard: 0.0049
  trash: 0.0019
```

You can also pass a different model checkpoint:

```powershell
python predict.py path\to\image.jpg --model rise_ai_model.pth
```

## Why `predict.py` Needs an Image Path

The prediction script needs to know which image to classify. If you run:

```powershell
python predict.py
```

you will get:

```text
error: the following arguments are required: image
```

That is expected. Run it with an image path:

```powershell
python predict.py dataset-resized\plastic\plastic1.jpg
```

## Offline Training

Training uses local images from:

```text
dataset-resized
```

However, this line may need internet the first time it runs:

```python
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
```

That downloads pretrained ResNet18 weights if they are not already cached. After the weights are cached, training can run offline.

To force fully offline training from scratch, change it to:

```python
model = models.resnet18(weights=None)
```

Pretrained weights are recommended because they usually improve accuracy and reduce training time.

## Model Checkpoint

The trained model is saved as:

```text
rise_ai_model.pth
```

The checkpoint contains:

```python
{
    "model_state_dict": model.state_dict(),
    "classes": base_dataset.classes
}
```

Saving the class list is important because prediction must use the same class order as training.

## Common Issues

### `Validation Accuracy: 1.0000`

This can be real, but often means something is wrong. Check that:

- `dataset_path` points directly to the class folders
- There is more than one class
- The validation set contains all classes
- There are no duplicate images leaking between train and validation

### `Image file not found`

The image path passed to `predict.py` does not exist.

Use:

```powershell
Get-ChildItem dataset-resized\glass
```

Then pass one of the filenames shown.

### `Model file not found`

`rise_ai_model.pth` does not exist in the project folder, or you passed the wrong model path.

Train first:

```powershell
python train_model.py
```

### Poor Prediction On New Images

If predictions are poor on real-world images, possible causes include:

- The dataset is too small
- The test image looks different from the training images
- The object is cropped, blurry, dark, or mixed with other trash
- Some training labels are incorrect
- The model needs more varied examples

## Recommended Workflow

1. Confirm the dataset folders are correct.
2. Train the model:

```powershell
python train_model.py
```

3. Test with images from each class:

```powershell
python predict.py dataset-resized\glass\glass1.jpg
python predict.py dataset-resized\plastic\plastic1.jpg
python predict.py dataset-resized\paper\paper1.jpg
```

4. Test with new images that were not part of training.
5. If results are weak, improve the dataset before changing the model heavily.

## Notes

The current scripts are intentionally simple and local. They are good for training and testing a first image classifier. For a production version, useful next steps would be:

- Add early stopping
- Save training history to a CSV file
- Plot loss and accuracy curves
- Add a confusion matrix
- Evaluate on a separate test set
- Build a small app or API around `predict.py`



pin for my ecogacha account: 123581321