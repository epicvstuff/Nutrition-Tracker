# Nutrition Tracker

A modern web application for tracking daily nutrition intake with features for food search, manual entry, and image-based food classification.

## Features

- **Food Search**: Search for foods using the OpenFoodFacts API
- **Manual Entry**: Add custom foods with nutritional information
- **Image Classification**: Upload food images for automatic classification
- **Daily Logging**: Track your daily food intake
- **Nutritional Totals**: View daily totals for calories, protein, carbs, and fat
- **Local Storage**: Data persists between sessions
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
nutrition-tracker/
├── index.html              # Main HTML file
├── assets/                 # Static assets
│   └── images/            # Image assets
├── css/                    # Stylesheets
│   ├── main.css           # Main styles
│   ├── components/        # Component-specific styles
│   │   ├── search.css
│   │   ├── food-form.css
│   │   ├── food-list.css
│   │   └── upload.css
│   └── variables.css      # CSS variables and theme
├── js/                     # JavaScript files
│   ├── main.js            # Main application entry
│   ├── api/               # API related code
│   │   └── foodApi.js     # OpenFoodFacts API integration
│   ├── services/          # Business logic
│   │   ├── foodService.js # Food management logic
│   │   └── storageService.js # Local storage handling
│   ├── components/        # UI components
│   │   ├── search.js
│   │   ├── foodForm.js
│   │   ├── foodList.js
│   │   └── upload.js
│   └── utils/             # Utility functions
│       └── helpers.js
└── README.md              # Project documentation
```

## Setup and Installation

1. Clone the repository
2. Open `index.html` in a modern web browser
3. No build process required - the application runs directly in the browser

## Usage

1. **Search for Food**:
   - Enter a food name in the search box
   - Click on a result to select it
   - Enter the quantity in grams

2. **Manual Entry**:
   - Click "Manual" to switch to manual mode
   - Enter food name and nutritional information
   - Click "Add Food to Log"

3. **Image Classification**:
   - Upload a food image
   - The system will attempt to classify it
   - Adjust the nutritional information if needed
   - Add to your log

4. **View and Manage Log**:
   - See your daily food entries in the table
   - View daily totals at the bottom
   - Click "Start New Day" to clear the log

## Technologies Used

- HTML5
- CSS3 (with CSS Variables and Flexbox/Grid)
- JavaScript (ES6+)
- OpenFoodFacts API
- Local Storage API

## Browser Support

The application works in all modern browsers that support:
- ES6 Modules
- CSS Grid
- Flexbox
- Local Storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
