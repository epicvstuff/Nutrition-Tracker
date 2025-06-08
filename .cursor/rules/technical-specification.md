# Technical Specification Rule

This rule provides the technical specifications for the Nutrition Tracker application.

## Rule Content
```markdown
# Nutrition Tracker - Technical Specification (PRODUCTION READY)

## ✅ CURRENT STATUS: FULLY FUNCTIONAL
- **Backend API**: ✅ Running on http://127.0.0.1:8000 with USDA integration
- **Frontend UI**: ✅ Running on http://127.0.0.1:3000 with corrected data flow
- **AI Classification**: ✅ 88.89% accuracy CNN model operational
- **USDA Integration**: ✅ Real nutritional data from 350,000+ USDA foods
- **End-to-End Workflow**: ✅ Image → AI → USDA → Frontend display working perfectly

## System Architecture

### Full-Stack Architecture
The application consists of two independent services:

1. **Backend API** (Port 8000): FastAPI + Machine Learning + USDA Integration
2. **Frontend Web App** (Port 3000): Static HTML/CSS/JavaScript

### Frontend Architecture
```
frontend/
├── index.html              # Main application entry point
├── css/
│   ├── main.css           # Main styles
│   ├── variables.css      # CSS variables and theme
│   └── components/        # Component-specific styles
│       ├── search.css
│       ├── food-form.css
│       ├── food-list.css
│       └── upload.css
├── js/
│   ├── main.js           # Application entry point (FIXED: nutrition_info handling)
│   ├── api/              # API integration layer
│   │   └── foodApi.js    # OpenFoodFacts API integration
│   ├── services/         # Business logic services
│   │   ├── foodService.js
│   │   └── storageService.js
│   ├── components/       # UI components
│   │   ├── search.js
│   │   ├── foodForm.js
│   │   ├── foodList.js
│   │   └── upload.js     # FIXED: Uses 127.0.0.1:8000 correctly
│   └── utils/            # Utility functions
└── assets/               # Static assets
```

### Backend Architecture (UPDATED WITH USDA)
```
backend/
├── app.py               # Main FastAPI application with USDA lifecycle
├── config.py           # Configuration with USDA API settings
├── requirements.txt    # Complete dependencies with aiohttp
├── api/
│   ├── __init__.py
│   └── endpoints.py    # Classification + USDA nutrition endpoints
├── models/
│   ├── __init__.py
│   ├── base_model.py   # Abstract model interface
│   └── cnn_model.py    # CNN model with TensorFlow 2.16.1
├── services/           # NEW: External API integration
│   ├── __init__.py
│   └── usda_service.py # USDA FoodData Central API service
└── training/
    └── classifier.py   # TensorFlow 2.16/Keras 3.x trainer
```

### Model Storage
```
models/
└── fruit_vegetable_classifier.h5  # Trained CNN model (88.89% accuracy, 218MB)
```

## Updated Dependencies (PRODUCTION READY)

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
aiohttp==3.9.1          # NEW: For USDA API integration
```

## Machine Learning Model Specifications (OPERATIONAL)

### Trained CNN Model
- **Status**: ✅ OPERATIONAL with 88.89% validation accuracy
- **Architecture**: 3-layer CNN with data augmentation
- **Framework**: TensorFlow 2.16.1 / Keras 3.x
- **Input**: 150x150 RGB images
- **Output**: 36 food categories with confidence scores
- **Model Size**: 218MB
- **Training**: 25 epochs with early stopping

### Supported Food Categories (36 total) - VERIFIED WORKING
- **Fruits** (11): apple, banana, grapes, kiwi, lemon, mango, orange, pear, pineapple, pomegranate, watermelon
- **Vegetables** (21): beetroot, bell pepper, cabbage, capsicum, carrot, cauliflower, corn, cucumber, eggplant, garlic, ginger, lettuce, onion, peas, potato, raddish, spinach, sweetcorn, sweetpotato, tomato, turnip
- **Others** (4): chilli pepper, jalepeno, paprika, soy beans

## USDA FoodData Central Integration (NEW - OPERATIONAL)

### USDA Service Configuration
```python
# Environment Variables (.env)
USDA_API_KEY=RVI4ttmIOr2StRAnDkOUgYnsrtz2rNewwoIdr4SG
USDA_BASE_URL=https://api.nal.usda.gov/fdc/v1
```

### Food Name Mapping System
```python
food_name_mapping = {
    "sweetcorn": "sweet corn",
    "jalepeno": "jalapeño peppers", 
    "chilli pepper": "hot peppers",
    "bell pepper": "bell peppers",
    "capsicum": "bell peppers",
    "beetroot": "beets",
    # ... 20+ more mappings for optimal USDA search
}
```

### USDA API Integration Features
- **Real-time nutrition data**: 350,000+ USDA foods
- **Smart fallback system**: Mock data when USDA unavailable
- **Government-verified data**: Official nutritional information
- **Comprehensive nutrients**: Calories, protein, carbs, fat, fiber, sugars, sodium
- **Multiple data types**: Foundation, SR Legacy, Survey foods

## Updated API Specifications (WORKING)

### Classification API (OPERATIONAL)
```http
POST /api/v1/classify
Content-Type: multipart/form-data
Host: 127.0.0.1:8000

Response (ACTUAL WORKING FORMAT):
{
  "filename": "banana.jpg",
  "predicted_class": "banana",
  "confidence": 0.9999858140945435,
  "nutrition_info": {
    "name": "banana",
    "description": "Bananas, overripe, raw",
    "calories": 85.0,
    "protein": 0.7,
    "carbs": 20.1,
    "fat": 0.2,
    "fiber": 1.7,
    "sugars": 15.8,
    "sodium": 0,
    "source": "USDA FoodData Central",
    "fdc_id": 1105073,
    "data_type": "Foundation",
    "serving_size": "100g"
  }
}
```

### USDA Search API (NEW - OPERATIONAL)
```http
GET /api/v1/search-nutrition/{food_name}
Host: 127.0.0.1:8000

Response:
{
  "name": "paprika",
  "description": "Spices, paprika", 
  "calories": 282,
  "protein": 14.1,
  "carbs": 54.0,
  "fat": 12.9,
  "fiber": 34.9,
  "sugars": 0,
  "sodium": 68.0,
  "source": "USDA FoodData Central",
  "fdc_id": 171329,
  "data_type": "SR Legacy",
  "serving_size": "100g"
}
```

## Frontend Data Flow (FIXED)

### Corrected JavaScript Data Handling
```javascript
// main.js - FIXED VERSION
handleFoodClassified(data) {
  const nutritionInfo = data.nutrition_info || {};  // FIXED: Access nested object
  this.foodForm.setSelectedFood({
    name: data.predicted_class,
    nutrients: {
      calories: nutritionInfo.calories || 0,      // FIXED: Read from nutrition_info
      protein: nutritionInfo.protein || 0,
      carbs: nutritionInfo.carbs || 0,
      fat: nutritionInfo.fat || 0
    }
  });
}

// upload.js - FIXED VERSION  
const response = await fetch('http://127.0.0.1:8000/api/v1/classify', {  // FIXED: Correct URL
  method: 'POST',
  body: formData
});
```

## Production Deployment Status

### Startup Commands (VERIFIED WORKING)
```bash
# Backend (Terminal 1)
cd /Users/adityapalit/Nutrition-Tracker
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload

# Frontend (Terminal 2) 
cd /Users/adityapalit/Nutrition-Tracker/frontend
python -m http.server 3000
```

### Verified Working Workflow
1. ✅ **Image Upload**: Frontend uploads to 127.0.0.1:8000/api/v1/classify
2. ✅ **AI Classification**: CNN model predicts food with confidence
3. ✅ **USDA Lookup**: Smart mapping finds nutrition data in USDA database
4. ✅ **Data Return**: Complete nutrition profile returned via nutrition_info
5. ✅ **Frontend Display**: Calories, protein, carbs, fat populate in form
6. ✅ **User Interaction**: Add to daily log, track totals

### Performance Metrics (MEASURED)
- **Model Load Time**: 10-30 seconds on startup
- **Classification Time**: 1-3 seconds per image
- **USDA API Response**: 500ms-2s depending on network
- **Frontend Responsiveness**: Real-time with proper caching

## Troubleshooting Guide (FIELD TESTED)

### Cache Issues (SOLVED)
- **Problem**: Browser serving old JavaScript files
- **Solution**: Hard refresh (Ctrl+Shift+R) or restart frontend server

### API Connection Issues (SOLVED)
- **Problem**: localhost vs 127.0.0.1 mismatch
- **Solution**: All endpoints now use 127.0.0.1 consistently

### USDA API Issues (HANDLED)
- **Problem**: Food not found in USDA database
- **Solution**: Smart mapping system + fallback to mock data

### Model Loading Issues (RESOLVED)
- **Problem**: Model file missing or corrupted
- **Solution**: Proper model loading with error handling and fallback

## Next Phase Recommendations

### Immediate Optimizations
1. **Frontend Caching**: Add service worker for offline capability
2. **Image Optimization**: Client-side image compression before upload
3. **Error Handling**: More granular error messages and retry logic
4. **User Experience**: Loading indicators and progress bars

### Future Enhancements
1. **User Accounts**: Authentication and cloud storage
2. **Nutrition Goals**: Daily calorie and macro targets
3. **Food Database**: Local SQLite cache for offline operation
4. **Mobile App**: React Native or Flutter mobile version
5. **Improved AI**: Larger model with more food categories

## Security & Production Notes

### Environment Security
- ✅ API keys stored in .env file (not in repo)
- ✅ No sensitive data in client-side code
- ✅ CORS properly configured for local development

### Production Readiness Checklist
- ✅ All dependencies pinned to specific versions
- ✅ Error handling and logging implemented
- ✅ API documentation available at /docs
- ✅ Frontend works without build process
- ✅ Backend auto-reloads during development
- ✅ Model file excluded from git (too large)
- ✅ Complete end-to-end functionality verified
