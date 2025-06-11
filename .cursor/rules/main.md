# Nutrition Tracker - Main Cursor Rules

## 📁 Rule Organization
This directory contains all cursor rules for the Nutrition Tracker project:
- **main.md** (this file) - Main project overview and quick reference
- **technical-specification.md** - Detailed technical architecture and specifications  
- **implementation-plan.md** - Phase-by-phase implementation status and roadmap
- **test-plan.md** - Testing strategy and test cases

---

## 🎯 PROJECT STATUS: PRODUCTION READY ✅

### Quick Overview
This is a **fully functional** nutrition tracking application with AI-powered food recognition and real USDA nutritional data integration. All core features are **OPERATIONAL** and tested.

### Architecture
- **Backend**: FastAPI (Python) with CNN model + USDA API integration
- **Frontend**: Static HTML/CSS/JavaScript with modern ES6 modules
- **AI Model**: TensorFlow 2.16.1 CNN with 88.89% accuracy on 36 food categories
- **Data Sources**: USDA FoodData Central (350,000+ foods) + OpenFoodFacts

### Current Working Status
✅ **Backend API**: http://127.0.0.1:8000 (with USDA integration)  
✅ **Frontend UI**: http://127.0.0.1:3000 (corrected data flow)  
✅ **AI Classification**: 88.89% accuracy, real-time predictions  
✅ **USDA Integration**: Government-verified nutritional data  
✅ **End-to-End Workflow**: Image → AI → USDA → Frontend display  

### Startup Commands
```bash
# Terminal 1: Backend
cd /Users/adityapalit/Nutrition-Tracker
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend  
cd /Users/adityapalit/Nutrition-Tracker/frontend
python -m http.server 3000
```

### Key Completed Features
1. **AI Food Recognition**: Upload images for automatic food classification
2. **Real USDA Data**: 350,000+ foods with government-verified nutrition info
3. **Smart Food Mapping**: Intelligent mapping from AI classes to USDA search terms
4. **Manual Food Entry**: Custom food entry with nutritional information
5. **Daily Tracking**: Real-time nutrition totals and food logging
6. **Local Storage**: Persistent data between sessions

### Verified Workflow
Image Upload → CNN Classification → USDA Database Lookup → Nutrition Display → Daily Log Addition

### Tech Stack
- **Backend**: FastAPI, TensorFlow 2.16.1, aiohttp, loguru, pydantic
- **Frontend**: Vanilla JavaScript (ES6+), CSS Grid/Flexbox, HTML5
- **APIs**: USDA FoodData Central, OpenFoodFacts
- **Storage**: LocalStorage (frontend), model files (218MB CNN)

### Development Guidelines
- All API endpoints use `127.0.0.1` (not localhost) for consistency
- Frontend reads nutrition data from `data.nutrition_info` object structure
- USDA API key configured in `.env` file (not in repository)
- Model file excluded from git due to size (218MB)
- Smart food name mapping handles model→USDA term translation

### Next Phase (Optional)
Future enhancements could include user accounts, mobile app, improved AI model, meal planning, and nutritional insights dashboard.

### Repository Structure
```
nutrition-tracker/
├── backend/           # FastAPI + ML model + USDA service
├── frontend/          # Static web app
├── trained_models/    # CNN model file (218MB, excluded from git)
├── .env              # Environment variables (API keys)
└── .cursor/rules/    # All cursor rules and documentation
    ├── main.md                    # Main overview (this file)
    ├── technical-specification.md # Detailed technical docs
    ├── implementation-plan.md     # Implementation roadmap
    └── test-plan.md              # Testing strategy
```

**Note**: This project is COMPLETE and FUNCTIONAL. All major features work correctly in development environment. 