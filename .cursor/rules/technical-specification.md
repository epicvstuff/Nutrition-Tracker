# Technical Specification Rule

This rule provides the technical specifications for the Nutrition Tracker application.

## Rule Content
```markdown
# Nutrition Tracker - Technical Specification

## Project Overview
A comprehensive nutrition tracking application that combines AI-powered food classification with real USDA nutritional data integration. Users can upload food images for automatic classification or manually search the extensive USDA database for accurate nutritional information.

## Architecture Overview

### Backend (FastAPI)
- **API Framework**: FastAPI with automatic OpenAPI documentation
- **Food Classification**: TensorFlow CNN model (88.89% accuracy, 36 food categories)
- **USDA Integration**: Complete integration with USDA FoodData Central API
- **Data Sources**: USDA FoodData Central (350,000+ foods) + OpenFoodFacts (fallback)
- **Environment**: Python 3.12, async/await patterns

### Frontend (Static)
- **Framework**: Vanilla HTML/CSS/JavaScript (ES6 modules)
- **Architecture**: Component-based design with separate modules
- **Data Flow**: Image upload → AI classification → USDA nutrition → Display
- **Search Flow**: User query → USDA search → Rich results → Manual selection

### AI Model
- **Type**: Convolutional Neural Network (CNN)
- **Framework**: TensorFlow 2.16.1
- **Performance**: 88.89% accuracy on test dataset
- **Categories**: 36 food types (fruits, vegetables, spices)
- **Input**: RGB images, automatically resized to model requirements

## 🔍 Enhanced Search & Data Integration

### Multi-Source Search System
1. **Primary: USDA FoodData Central API**
   - 350,000+ verified food items
   - Government-validated nutritional data
   - Foundation Foods, SR Legacy, FNDDS datasets
   - Comprehensive nutrient profiles (calories, protein, carbs, fat, fiber, sugars, sodium)
   - **NEW**: Direct user search integration with rich results

2. **Fallback: OpenFoodFacts API**
   - Community-driven database
   - International food products
   - Branded items and packaged foods
   - Automatic fallback when USDA has no results

### Search Features
- **Real-time Search**: As-you-type search with instant results
- **Smart Mapping**: Handles variations in food names (e.g., "jalepeno" → "jalapeño peppers")
- **Data Source Indicators**: Visual distinction between USDA and OpenFoodFacts results
- **Rich Results Display**: Shows calories, macronutrients, data quality, and serving sizes
- **Fallback Mechanism**: Automatically tries OpenFoodFacts if USDA has no results

## 🤖 AI-Powered Classification

### Image Classification Workflow
1. **Image Upload**: Users upload food images (JPEG, PNG)
2. **AI Processing**: CNN model classifies the food type
3. **USDA Lookup**: Classified food name mapped to USDA database
4. **Nutrition Retrieval**: Real nutritional data fetched from USDA API
5. **Results Display**: Classification confidence + complete nutrition profile

### Food Name Mapping
Smart mapping system handles model predictions to USDA terminology:
```
Model Output → USDA Search Term
"sweetcorn" → "sweet corn"
"jalepeno" → "jalapeño peppers"
"beetroot" → "beets"
```

## 📊 Data Structure

### USDA Nutrition Response
```json
{
  "name": "apple",
  "description": "Apples, fuji, with skin, raw",
  "calories": 64.7,
  "protein": 0.1,
  "carbs": 15.7,
  "fat": 0.2,
  "fiber": 2.1,
  "sugars": 13.3,
  "sodium": 1.0,
  "source": "USDA FoodData Central",
  "fdc_id": 1750340,
  "data_type": "Foundation",
  "serving_size": "100g"
}
```

### Search Results Format
```json
{
  "query": "apple",
  "results": [
    {
      "id": 1750340,
      "name": "Apples, fuji, with skin, raw",
      "data_type": "Foundation",
      "nutrients": {
        "calories": 64.7,
        "protein": 0.1,
        "carbs": 15.7,
        "fat": 0.2,
        "fiber": 2.1,
        "sugars": 13.3,
        "sodium": 1.0
      },
      "serving_size": "100g",
      "source": "USDA FoodData Central"
    }
  ],
  "total_found": 1
}
```

## 🔧 API Endpoints

### Food Classification
- `POST /api/v1/classify` - Upload image for AI classification + USDA nutrition lookup

### USDA Search Integration
- `GET /api/v1/search-foods?query={food}&limit={n}` - Search USDA database for multiple foods
- `GET /api/v1/search-nutrition/{food_name}` - Get specific nutrition info

### Health & Documentation
- `GET /` - API health check and basic info
- `GET /docs` - Interactive API documentation (OpenAPI/Swagger)

## 🎨 Frontend Components

### Core Components
1. **SearchComponent** (`frontend/js/components/search.js`)
   - USDA-first search with OpenFoodFacts fallback
   - Rich result display with data source indicators
   - Visual distinction for USDA vs OpenFoodFacts results

2. **UploadComponent** (`frontend/js/components/upload.js`)
   - Image upload and preview
   - AI classification with confidence scores
   - Integration with USDA nutrition lookup

3. **FoodFormComponent** (`frontend/js/components/foodForm.js`)
   - Manual food entry
   - Quantity and serving size calculations

4. **FoodListComponent** (`frontend/js/components/foodList.js`)
   - Daily food log with nutritional summaries
   - Local storage persistence

### Enhanced APIs
1. **FoodApi** (`frontend/js/api/foodApi.js`)
   - Unified search interface (USDA + OpenFoodFacts)
   - Automatic fallback mechanism
   - Result standardization

## 🛠 Technical Implementation

### Backend Services
1. **USDAService** (`backend/services/usda_service.py`)
   - Async USDA API integration
   - Food search and nutrition retrieval
   - Smart name mapping for model predictions
   - Session management and error handling

2. **CNNModel** (`backend/models/cnn_model.py`)
   - TensorFlow model loading and inference
   - Image preprocessing and prediction
   - Fallback nutrition data for unsupported items

### Configuration
- **Environment Variables**: API keys, database URLs via `.env` file
- **CORS**: Configured for frontend development
- **Logging**: Structured logging with loguru
- **Error Handling**: Comprehensive error responses with fallbacks

## 🔄 User Workflows

### AI Classification Workflow
1. User uploads food image
2. CNN model classifies food (36 categories)
3. Prediction mapped to USDA food name
4. USDA API fetched for nutrition data
5. Complete nutrition profile displayed
6. User enters quantity and adds to daily log

### Manual Search Workflow
1. User types food name in search box
2. Real-time USDA database search
3. Multiple relevant results displayed with:
   - USDA vs OpenFoodFacts source indicators
   - Complete nutrition previews
   - Data quality indicators (Foundation, SR Legacy, etc.)
4. User selects preferred food item
5. Nutrition data auto-populates in form
6. User enters quantity and adds to log

### Data Integration
- **Primary Source**: USDA FoodData Central (government-verified)
- **Secondary Source**: OpenFoodFacts (community-driven)
- **Fallback**: Model-based nutrition estimates
- **Storage**: Client-side localStorage for daily logs

## ✨ Key Features

### Accuracy & Data Quality
- **88.89% AI classification accuracy** on 36 food categories
- **350,000+ USDA verified foods** with government-validated nutrition data
- **Smart food name mapping** for seamless AI-to-database integration
- **Comprehensive nutrient profiles** (7 key nutrients tracked)

### User Experience
- **Visual data source indicators** (🏛️ USDA, 🌍 OpenFoodFacts)
- **Rich search results** with nutrition previews
- **Automatic fallback systems** ensure users always get results
- **Real-time search** with instant feedback
- **Mobile-responsive design** for all devices

### Production Ready
- **Complete error handling** with graceful fallbacks
- **Structured logging** for debugging and monitoring
- **Environment-based configuration** for different deployment stages
- **Comprehensive API documentation** with OpenAPI/Swagger

## 🚀 Current Status: PRODUCTION READY

All major features implemented and tested:
- ✅ AI food classification with USDA integration
- ✅ Real-time USDA database search
- ✅ Multi-source nutrition data (USDA + OpenFoodFacts)
- ✅ Complete frontend with enhanced search UI
- ✅ Production-ready error handling and fallbacks
- ✅ Comprehensive logging and monitoring
- ✅ Mobile-responsive design
- ✅ Full documentation and API specs

The application successfully combines cutting-edge AI classification with authoritative government nutrition data to provide users with the most accurate and comprehensive nutrition tracking experience available.
