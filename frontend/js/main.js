import FoodService from './services/foodService.js';
import SearchComponent from './components/search.js';
import FoodFormComponent from './components/foodForm.js';
import FoodListComponent from './components/foodList.js';
import UploadComponent from './components/upload.js';

class NutritionTracker {
  constructor() {
    this.foodService = new FoodService();
    this.foodList = new FoodListComponent();
    this.foodForm = new FoodFormComponent(this.handleAddFood.bind(this));
    this.search = new SearchComponent(this.handleFoodSelect.bind(this));
    this.upload = new UploadComponent(this.handleFoodClassified.bind(this));

    this.initialize();
  }

  initialize() {
    // Load saved data
    const foodLog = this.foodService.loadFoodLog();
    this.updateUI(foodLog);

    // Set up reset handler
    this.foodList.setResetHandler(this.handleReset.bind(this));
  }

  updateUI(foodLog) {
    this.foodList.renderFoodList(foodLog);
    this.foodList.renderTotals(this.foodService.calculateTotals());
  }

  handleAddFood(food) {
    try {
      const updatedLog = this.foodService.addFood(food);
      this.updateUI(updatedLog);
    } catch (error) {
      console.error('Error adding food:', error);
      alert('Failed to add food. Please try again.');
    }
  }

  handleFoodSelect(food) {
    this.foodForm.setSelectedFood(food);
  }

  handleFoodClassified(data) {
    // Pre-fill the form with the classified food data
    console.log('Received classification data:', data);
    const nutritionInfo = data.nutrition_info || {};
    console.log('Extracted nutrition info:', nutritionInfo);
    
    this.foodForm.setSelectedFood({
      name: data.predicted_class,
      nutrients: {
        calories: nutritionInfo.calories || 0,
        protein: nutritionInfo.protein || 0,
        carbs: nutritionInfo.carbs || 0,
        fat: nutritionInfo.fat || 0
      }
    });
  }

  handleReset() {
    const updatedLog = this.foodService.clearFoodLog();
    this.updateUI(updatedLog);
    this.foodForm.clearSelection();
  }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new NutritionTracker();
}); 