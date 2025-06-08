# Models Directory

This directory contains the trained machine learning models for the Nutrition Tracker application.

## Required Model

The application requires a trained CNN model file:
- **File**: `fruit_vegetable_classifier.h5`
- **Size**: ~218 MB
- **Format**: Keras/TensorFlow model

## Getting the Trained Model

Since the model file is too large for GitHub (218 MB > 100 MB limit), you have several options:

### Option 1: Train Your Own Model 🎯
1. Follow the instructions in `backend/training/README.md`
2. Download a food image dataset 
3. Run the training script: `cd backend/training && python classifier.py`
4. The model will be saved as `fruit_vegetable_classifier.h5` in this directory

### Option 2: Download Pre-trained Model (Recommended) 📥
Since training takes time and requires large datasets, you can:
1. Contact the repository maintainer for a download link
2. Check the releases section for model downloads
3. Use cloud storage links (Google Drive, Dropbox, etc.)

### Option 3: Use Mock Predictions (Development) 🔧
The application will automatically fall back to mock predictions if no model is found.
- Returns "apple" with 95% confidence for all images
- Useful for frontend development and testing
- No actual classification is performed

## Current Model Performance

The pre-trained model includes:
- **36 food categories**: fruits, vegetables, and common foods
- **88.89% validation accuracy**
- **Input size**: 150x150 pixels
- **Color space**: RGB

## Model Integration

The model is automatically loaded by the FastAPI backend when:
1. The file exists in this directory
2. The application starts up
3. No import errors occur

If the model is missing, you'll see a warning in the logs:
```
WARNING: Could not load model from models/fruit_vegetable_classifier.h5
INFO: Using mock predictions instead
```

## Supported Formats

- `.h5` - Keras/TensorFlow format (recommended)
- `.hdf5` - Alternative HDF5 format
- Other formats may require code modifications 