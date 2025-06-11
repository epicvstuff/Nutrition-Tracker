# Nutrition Tracker ✅ PRODUCTION READY

A modern full-stack web application for tracking daily nutrition intake with AI-powered food image classification, real USDA nutritional data, food search, and manual entry capabilities.

## 🎯 CURRENT STATUS: FULLY FUNCTIONAL
- ✅ **Backend API**: Running with USDA FoodData Central integration (350,000+ foods)
- ✅ **Frontend UI**: Complete with multi-source search (USDA primary, OpenFoodFacts fallback)
- ✅ **AI Classification**: 88.89% accuracy CNN model operational on 36 food categories
- ✅ **End-to-End Workflow**: Image → AI → USDA → Frontend display working perfectly

## ✨ Features

- **🔬 AI Food Classification**: Upload food images for automatic classification using a trained CNN model (88.89% accuracy)
- **🏛️ USDA Integration**: Real nutritional data from USDA FoodData Central (350,000+ government-verified foods)
- **🔍 Advanced Food Search**: Multi-source search system with rich nutrition previews and data quality indicators
- **🌍 Smart Fallback**: Automatic fallback to OpenFoodFacts when foods not found in USDA database
- **✏️ Manual Entry**: Add custom foods with nutritional information
- **📊 Daily Logging**: Track your daily food intake with real-time totals
- **🧮 Nutritional Analytics**: View detailed nutrition profiles (calories, protein, carbs, fat, fiber, sugars, sodium)
- **💾 Local Storage**: Data persists between sessions
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🚀 RESTful API**: FastAPI backend with interactive documentation
- **🎯 Smart Mapping**: Intelligent food name mapping for optimal USDA search results

## 🏗️ Architecture

This application consists of two main components:

### Backend (FastAPI + ML Model)
- **Port**: 8000
- **Technology**: Python, FastAPI, TensorFlow/Keras
- **Features**: CNN-based food classification, USDA API integration, RESTful API, automatic image preprocessing

### Frontend (Static Web App)
- **Port**: 3000
- **Technology**: HTML5, CSS3, Vanilla JavaScript
- **Features**: Modern responsive UI, real-time interaction with backend API, multi-source search interface

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
│   │   └── endpoints.py   # Classification and search endpoints
│   ├── services/          # External API services
│   │   ├── __init__.py
│   │   └── usda_service.py # USDA nutrition data service
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
├── trained_models/        # Trained ML model files
│   └── fruit_vegetable_classifier.h5  # CNN model file (218MB - see setup below)
├── tests/                 # Test files
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pip
- Modern web browser
- 8GB+ RAM (for model training, optional)
- **USDA API Key** (optional, for real nutrition data)

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your USDA API key:
# USDA_API_KEY=your_actual_api_key_here
# USDA_BASE_URL=https://api.nal.usda.gov/fdc/v1
```

**📍 Getting a USDA API Key:**
1. Visit [USDA FoodData Central](https://fdc.nal.usda.gov/api-guide.html)
2. Sign up for a free API key
3. Add your key to the `.env` file

### 3. Set Up the AI Model (Required for Image Classification)

The application requires a trained CNN model file (`fruit_vegetable_classifier.h5`) in the `trained_models/` directory. Since the model is too large for GitHub (218MB), choose one of these options:

#### Option A: Train Your Own Model 🎯
```bash
# Download a food image dataset (see Training section below)
# Then train the model:
cd backend/training
python classifier.py
# Model will be saved to trained_models/fruit_vegetable_classifier.h5
```

#### Option B: Download Pre-trained Model (Recommended) 📥
```bash
# Contact repository maintainer for download link
# Or check releases section for model downloads
# Place downloaded file in trained_models/fruit_vegetable_classifier.h5
```

#### Option C: Use Mock Predictions (Development) 🔧
```bash
# Application automatically uses mock predictions if no model found
# Returns "apple" with 95% confidence for all images
# Useful for frontend development and testing
```

### 4. Start the Backend API
```bash
# From project root directory
cd /path/to/Nutrition-Tracker
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Start the Frontend Server
```bash
# In a new terminal, from project root
cd frontend
python -m http.server 3000
```

### 6. Access the Application
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
- **File Size**: ~218 MB
- **Format**: Keras HDF5 (.h5)

### Model Integration
The model is automatically loaded by the FastAPI backend when:
1. The file exists in `trained_models/fruit_vegetable_classifier.h5`
2. The application starts up
3. No import errors occur

If the model is missing, you'll see a warning in the logs:
```
WARNING: Could not load model from trained_models/fruit_vegetable_classifier.h5
INFO: Using mock predictions instead
```

### Supported Food Categories
The model can classify 36 different foods:
- **Fruits**: apple, banana, grapes, kiwi, lemon, mango, orange, pear, pineapple, pomegranate, watermelon
- **Vegetables**: beetroot, bell pepper, cabbage, capsicum, carrot, cauliflower, corn, cucumber, eggplant, garlic, ginger, lettuce, onion, peas, potato, raddish, spinach, sweetcorn, sweetpotato, tomato, turnip
- **Others**: chilli pepper, jalepeno, paprika, soy beans

## 🎓 Model Training (Advanced)

If you want to retrain the model or customize it for new food categories:

### Training Data Setup

#### Option 1: Kaggle Fruits and Vegetables Dataset
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

#### Option 2: Custom Dataset
- Organize your images in the same folder structure
- Each class should have its own folder
- Recommended: 80-100 images per class minimum

### Training Process
```bash
cd backend/training
python classifier.py
```

### Training Requirements
- TensorFlow 2.16.1
- At least 8GB RAM
- GPU recommended for faster training
- Dataset: ~2.17 GB for full training

### Training Output
The trained model will be saved as `trained_models/fruit_vegetable_classifier.h5` and automatically loaded by the application.

You only need to retrain if you want to:
- Add new food categories
- Improve accuracy with more data
- Customize for specific use cases

## 🥗 Nutrition Data Sources

### USDA FoodData Central API (Primary)
- **Coverage**: 350,000+ food items with detailed nutrient profiles
- **Data Quality**: Government-verified nutritional information
- **Data Types**: Foundation, SR Legacy, Survey, Branded foods
- **Update Frequency**: Regular USDA database updates

### OpenFoodFacts API (Fallback)
- **Coverage**: Community-driven database with global foods
- **Data Quality**: Crowd-sourced, varies by product
- **Fallback Logic**: Automatically used when USDA has no results
- **Special Features**: Barcode scanning support, international foods

### API Endpoints
- `POST /api/v1/classify` - Image classification with USDA nutrition lookup
- `GET /api/v1/search-foods` - Multi-source food search with rich previews
- `GET /api/v1/search-nutrition/{food_name}` - Legacy nutrition search endpoint

## 🔧 Development

### Backend Development
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run with auto-reload
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

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

### 1. AI Image Classification
1. Click "Choose File" in the upload section
2. Select a food image (JPG, PNG)
3. Click "Classify Image"
4. Review the AI prediction and confidence score
5. System automatically fetches USDA nutrition data
6. Adjust quantity in grams if needed
7. Click "Add Food to Log"

### 2. Advanced Food Search
1. Enter a food name in the search box
2. System searches USDA database first, then OpenFoodFacts
3. Select from rich search results showing:
   - **Data Source**: 🏛️ USDA (government) or 🌍 OpenFoodFacts (community)
   - **Complete Nutrition Preview**: calories, protein, carbs, fat, fiber, sugars, sodium
   - **Data Quality Indicators**: Foundation, SR Legacy, Survey, Branded
   - **Serving Size Information**: per 100g or per serving
4. Click a result to auto-populate the form
5. Enter quantity and add to your daily log

### 3. Manual Entry
1. Click "Manual" to enable manual entry mode
2. Enter food name and nutritional values
3. Click "Add Food to Log"

### 4. Daily Tracking
- View all logged foods in the daily summary table
- Monitor real-time totals for calories and macronutrients
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
- **aiohttp**: Async HTTP client for API calls

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Grid/Flexbox
- **Vanilla JavaScript (ES6+)**: No framework dependencies
- **CSS Variables**: Consistent theming system
- **Module Pattern**: Clean code organization

### External APIs
- **USDA FoodData Central**: Government nutrition database
- **OpenFoodFacts**: Community nutrition database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created with ❤️ for healthier eating habits.

## 🙏 Acknowledgments

- **USDA FoodData Central**: For providing comprehensive nutrition data
- **OpenFoodFacts**: For community-driven food database
- **TensorFlow/Keras**: For machine learning framework
- **FastAPI**: For excellent Python web framework
