# Nutrition Tracker

A modern full-stack web application for tracking daily nutrition intake with AI-powered food image classification, food search, and manual entry capabilities.

## ✨ Features

- **🔬 AI Food Classification**: Upload food images for automatic classification using a trained CNN model (88.89% accuracy)
- **🔍 Food Search**: Search for foods using the OpenFoodFacts API
- **✏️ Manual Entry**: Add custom foods with nutritional information
- **📊 Daily Logging**: Track your daily food intake with real-time totals
- **🧮 Nutritional Analytics**: View daily totals for calories, protein, carbs, and fat
- **💾 Local Storage**: Data persists between sessions
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🚀 RESTful API**: FastAPI backend with interactive documentation

## 🏗️ Architecture

This application consists of two main components:

### Backend (FastAPI + ML Model)
- **Port**: 8000
- **Technology**: Python, FastAPI, TensorFlow/Keras
- **Features**: CNN-based food classification, RESTful API, automatic image preprocessing

### Frontend (Static Web App)
- **Port**: 3000
- **Technology**: HTML5, CSS3, Vanilla JavaScript
- **Features**: Modern responsive UI, real-time interaction with backend API

## 📁 Project Structure

```
nutrition-tracker/
├── backend/                # Python FastAPI backend
│   ├── app.py             # Main FastAPI application
│   ├── config.py          # Application configuration
│   ├── requirements.txt   # Python dependencies
│   ├── models/            # ML model classes
│   │   ├── base_model.py  # Abstract base model
│   │   └── cnn_model.py   # CNN implementation
│   ├── api/               # API endpoints
│   │   ├── __init__.py
│   │   └── endpoints.py   # Classification endpoints
│   └── training/          # Model training scripts
│       └── classifier.py  # CNN training script
├── frontend/              # Static web frontend
│   ├── index.html         # Main HTML file
│   ├── package.json       # Frontend dependencies
│   ├── css/               # Stylesheets
│   │   ├── main.css       # Main styles
│   │   ├── variables.css  # CSS variables
│   │   └── components/    # Component styles
│   ├── js/                # JavaScript modules
│   │   ├── main.js        # Application entry point
│   │   ├── api/           # API integration
│   │   ├── services/      # Business logic
│   │   ├── components/    # UI components
│   │   └── utils/         # Utility functions
│   └── assets/            # Static assets
├── models/                # Trained ML models (see models/README.md)
│   └── fruit_vegetable_classifier.h5  # Large model (not in repo)
├── tests/                 # Test files
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pip
- Modern web browser
- 8GB+ RAM (for model training, optional)

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Get the Trained Model (Required)
Since the model is too large for GitHub (218MB), choose one option:
```bash
# Option A: Train your own model (requires dataset)
cd backend/training
python classifier.py

# Option B: Download pre-trained model (contact maintainer)
# See models/README.md for details

# Option C: Use mock predictions (for development)
# Application will automatically use mock data if no model found
```

### 3. Start the Backend API
```bash
# From project root directory
cd /path/to/Nutrition-Tracker
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Start the Frontend Server
```bash
# In a new terminal, from project root
cd frontend
python -m http.server 3000
```

### 5. Access the Application
- **Frontend UI**: http://127.0.0.1:3000
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## 🧠 AI Model Information

### Trained CNN Model
- **Architecture**: Convolutional Neural Network
- **Classes**: 36 food categories (apple, banana, carrot, etc.)
- **Accuracy**: 88.89% validation accuracy
- **Input**: 150x150 RGB images
- **Framework**: TensorFlow 2.16.1 / Keras 3.x

### Supported Food Categories
The model can classify 36 different foods:
- Fruits: apple, banana, grapes, kiwi, lemon, mango, orange, pear, pineapple, pomegranate, watermelon
- Vegetables: beetroot, bell pepper, cabbage, capsicum, carrot, cauliflower, corn, cucumber, eggplant, garlic, ginger, lettuce, onion, peas, potato, raddish, spinach, sweetcorn, sweetpotato, tomato, turnip
- Others: chilli pepper, jalepeno, paprika, soy beans

## 🔧 Development

### Backend Development
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run with auto-reload
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### Model Training (Optional)
If you want to retrain the model:
```bash
cd backend/training
python classifier.py
```
Note: Requires a dataset in the `archive/` directory with train/validation/test folders.

### Frontend Development
The frontend is a static web application:
```bash
cd frontend
python -m http.server 3000
```

### Testing
```bash
# Run backend tests
cd backend
python -m pytest

# Run frontend tests
cd frontend
npm test
```

## 📖 Usage Guide

### 1. Image Classification
1. Click "Choose File" in the upload section
2. Select a food image (JPG, PNG)
3. Click "Classify Image"
4. Review the predicted food and confidence score
5. Adjust nutritional information if needed
6. Add to your daily log

### 2. Food Search
1. Enter a food name in the search box
2. Click "Search" to query OpenFoodFacts API
3. Select from search results
4. Enter quantity in grams
5. Add to your log

### 3. Manual Entry
1. Click "Manual" to enable manual entry mode
2. Enter food name and nutritional values
3. Click "Add Food to Log"

### 4. Daily Tracking
- View all logged foods in the table
- Monitor daily totals for calories and macronutrients
- Use "Start New Day" to clear the log

## 🛠️ Technologies Used

### Backend
- **Python 3.12**: Core language
- **FastAPI**: Modern, fast web framework
- **TensorFlow 2.16.1**: Machine learning framework
- **Keras 3.x**: High-level neural networks API
- **Pillow**: Image processing
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Grid/Flexbox
- **Vanilla JavaScript (ES6+)**: No framework dependencies
- **Modules**: ES6 module system

### APIs
- **OpenFoodFacts API**: Food database integration
- **Custom ML API**: Image classification endpoint

## 🔍 API Documentation

The backend provides a RESTful API:

### Endpoints
- `GET /`: API information
- `POST /api/v1/classify`: Image classification
- `GET /api/v1/openapi.json`: OpenAPI schema

### Interactive Documentation
Visit http://127.0.0.1:8000/docs for Swagger UI documentation.

## 🌐 Browser Support

- Chrome 80+
- Firefox 80+
- Safari 14+
- Edge 80+

Requirements:
- ES6 Modules support
- CSS Grid and Flexbox
- Fetch API
- Local Storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Install requirements: `pip install -r backend/requirements.txt`
- Run from project root: `python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000`

**Frontend won't load:**
- Start server from frontend directory: `cd frontend && python -m http.server 3000`
- Check that port 3000 isn't already in use

**Model predictions incorrect:**
- Ensure model file exists at `models/fruit_vegetable_classifier.h5`
- Check image quality and lighting
- Model works best with clear, well-lit food images

**CORS errors:**
- Ensure both frontend (port 3000) and backend (port 8000) are running
- Check browser console for specific error messages

## 🎯 Performance Notes

- First model load may take 10-30 seconds
- Image classification typically takes 1-3 seconds
- Frontend caches API responses for better performance
- Model requires ~250MB RAM when loaded
