# Training Data Setup

This directory contains the training script for the food classification model. The actual training dataset is not included in the repository due to its large size (2.17 GB).

## Getting Training Data

To retrain the model, you'll need to download a food image dataset. Here are some options:

### Option 1: Kaggle Fruits and Vegetables Dataset
1. Visit [Kaggle Food Classification Dataset](https://www.kaggle.com/datasets/moltean/fruits)
2. Download and extract to `backend/training/archive/`
3. Ensure the structure is:
   ```
   archive/
   ├── train/
   │   ├── apple/
   │   ├── banana/
   │   └── ... (other food categories)
   ├── validation/
   │   ├── apple/
   │   ├── banana/
   │   └── ... (other food categories)
   └── test/ (optional)
   ```

### Option 2: Custom Dataset
- Organize your images in the same folder structure
- Each class should have its own folder
- Recommended: 80-100 images per class minimum

## Training the Model

Once you have the dataset:

```bash
cd backend/training
python classifier.py
```

The trained model will be saved as `fruit_vegetable_classifier.h5` in the `models/` directory.

## Requirements

- TensorFlow 2.16.1
- At least 8GB RAM
- GPU recommended for faster training

## Current Model

The application includes a pre-trained model with:
- **36 food categories** 
- **88.89% validation accuracy**
- Trained on fruits, vegetables, and common foods

You only need to retrain if you want to:
- Add new food categories
- Improve accuracy with more data
- Customize for specific use cases 