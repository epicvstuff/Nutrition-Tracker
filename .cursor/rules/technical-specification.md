# Technical Specification Rule

This rule provides the technical specifications for the Nutrition Tracker application.

## Rule Content
```markdown
# Nutrition Tracker - Technical Specification (Updated)

## System Architecture

### Full-Stack Architecture
The application consists of two independent services:

1. **Backend API** (Port 8000): FastAPI + Machine Learning
2. **Frontend Web App** (Port 3000): Static HTML/CSS/JavaScript

### Frontend Architecture
```
frontend/
├── index.html              # Main application entry point
├── package.json           # Dependencies and scripts
├── css/
│   ├── main.css           # Main styles
│   ├── variables.css      # CSS variables and theme
│   └── components/        # Component-specific styles
│       ├── search.css
│       ├── food-form.css
│       ├── food-list.css
│       └── upload.css
├── js/
│   ├── main.js           # Application entry point (ES6 modules)
│   ├── api/              # API integration layer
│   │   └── foodApi.js    # OpenFoodFacts API + Backend API
│   ├── services/         # Business logic services
│   │   ├── foodService.js
│   │   └── storageService.js
│   ├── components/       # UI components
│   │   ├── search.js
│   │   ├── foodForm.js
│   │   ├── foodList.js
│   │   └── upload.js
│   └── utils/            # Utility functions
└── assets/               # Static assets
```

### Backend Architecture
```
backend/
├── app.py               # Main FastAPI application
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies (UPDATED)
├── api/
│   ├── __init__.py
│   └── endpoints.py    # Classification API routes
├── models/
│   ├── __init__.py
│   ├── base_model.py   # Abstract model interface
│   └── cnn_model.py    # CNN model implementation (UPDATED)
└── training/
    └── classifier.py   # TensorFlow 2.16/Keras 3.x trainer (FIXED)
```

### Model Storage
```
models/
└── fruit_vegetable_classifier.h5  # Trained CNN model (88.89% accuracy)
```

## Updated Dependencies

### Backend Dependencies (backend/requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pillow==10.1.0
numpy==1.26.2
pydantic==2.5.2
python-dotenv==1.0.0
pydantic-settings==2.1.0
loguru==0.7.2
tensorflow==2.16.1
matplotlib==3.8.2
```

### Frontend Dependencies (frontend/package.json)
```json
{
  "dependencies": {
    "jest": "^29.7.0",
    "cypress": "^13.6.0",
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/dom": "^9.3.0"
  }
}
```

## Machine Learning Model Specifications

### Trained CNN Model
- **Architecture**: 3-layer CNN with data augmentation
- **Framework**: TensorFlow 2.16.1 / Keras 3.x (UPDATED)
- **Input**: 150x150 RGB images
- **Output**: 36 food categories
- **Accuracy**: 88.89% validation accuracy
- **Model Size**: ~228MB
- **Training**: 25 epochs with early stopping

### Supported Food Categories (36 total)
- **Fruits** (11): apple, banana, grapes, kiwi, lemon, mango, orange, pear, pineapple, pomegranate, watermelon
- **Vegetables** (21): beetroot, bell pepper, cabbage, capsicum, carrot, cauliflower, corn, cucumber, eggplant, garlic, ginger, lettuce, onion, peas, potato, raddish, spinach, sweetcorn, sweetpotato, tomato, turnip
- **Others** (4): chilli pepper, jalepeno, paprika, soy beans

### Model Training Architecture
```python
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
```

## Updated Component Specifications

### 1. Backend Components (UPDATED)

#### Model Interface (`models/base_model.py`)
- Abstract base class for all models
- Defines common interface: `load_model()`, `preprocess_image()`, `predict()`, `get_nutritional_info()`
- Supports future model implementations

#### CNN Model (`models/cnn_model.py`) - UPDATED
- Implements BaseModel interface
- Uses Keras 3.x API for model loading
- Handles image preprocessing (resize to 150x150, normalize to 0-1)
- Returns predictions with confidence scores
- Includes real nutritional data for common foods

#### API Endpoints (`api/endpoints.py`)
- **POST /api/v1/classify**: Image classification endpoint
- Handles multipart file uploads
- Validates image types (JPEG, PNG)
- Returns classification results with nutritional information
- Comprehensive error handling and logging

#### Configuration (`config.py`)
```python
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Nutrition Tracker API"
    MODEL_TYPE: str = "cnn"
    MODEL_PATH: str = "models/fruit_vegetable_classifier.h5"
    IMG_WIDTH: int = 150
    IMG_HEIGHT: int = 150
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
```

### 2. Frontend Components (UPDATED)

#### Upload Component (`js/components/upload.js`)
- Handles file uploads to backend API
- Communicates with http://127.0.0.1:8000/api/v1/classify
- Displays classification results and confidence scores
- Automatically populates food form with predictions

#### Food Service (`js/services/foodService.js`)
- Manages food data operations with localStorage
- Integrates with backend API for image classification
- Handles OpenFoodFacts API integration
- Calculates daily nutritional totals

## API Specifications

### Classification API
```http
POST /api/v1/classify
Content-Type: multipart/form-data

Response:
{
  "filename": "apple.jpg",
  "predicted_class": "apple",
  "confidence": 0.9567,
  "nutrition_info": {
    "name": "apple",
    "calories": 52,
    "protein": 0.3,
    "carbs": 14.0,
    "fat": 0.2
  }
}
```

### Root Endpoint
```http
GET /
Response:
{
  "name": "Nutrition Tracker API",
  "version": "1.0.0",
  "model_type": "cnn"
}
```

## Deployment Specifications

### Development Setup
1. **Backend**: `python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload`
2. **Frontend**: `cd frontend && python -m http.server 3000`

### URLs
- **Frontend**: http://127.0.0.1:3000
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **OpenAPI Schema**: http://127.0.0.1:8000/api/v1/openapi.json

### System Requirements
- **Python**: 3.8+ (tested with 3.12)
- **RAM**: 4GB minimum, 8GB recommended (for model inference)
- **Storage**: 500MB for model and dependencies
- **Browser**: Modern browser with ES6 modules support

## Performance Characteristics

### Backend Performance
- **Model Load Time**: 10-30 seconds (first load)
- **Inference Time**: 1-3 seconds per image
- **Memory Usage**: ~250MB RAM for loaded model
- **Concurrent Users**: Supports multiple concurrent requests

### Frontend Performance
- **Initial Load**: <2 seconds (static files)
- **Image Upload**: Depends on file size and network
- **UI Responsiveness**: Real-time updates
- **Storage**: LocalStorage for persistence

## Security Implementation

### Input Validation
- File type validation (JPEG, PNG only)
- File size limits
- Image dimension validation
- Form input sanitization

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing Strategy (IMPLEMENTED)

### Backend Testing
- Unit tests for model components
- API endpoint testing
- Image processing validation
- Error handling verification

### Frontend Testing
- Component testing with Jest
- Integration testing
- E2E testing with Cypress
- Manual UI testing

## Troubleshooting Guide

### Common Issues
1. **Import Errors**: Use correct TensorFlow 2.16/Keras 3.x imports
2. **Model Loading**: Ensure model file exists at `models/fruit_vegetable_classifier.h5`
3. **CORS Errors**: Verify both servers are running on correct ports
4. **Poor Predictions**: Check image quality and lighting conditions

### Performance Optimization
1. **Model Caching**: Model loaded once at startup
2. **Image Preprocessing**: Efficient resize and normalization
3. **API Response Caching**: Frontend caches API responses
4. **Static File Serving**: Optimized with HTTP server
```

## Usage
This rule should be referenced when:
1. Implementing new features
2. Making architectural decisions
3. Setting up development environment
4. Writing tests
5. Reviewing code 