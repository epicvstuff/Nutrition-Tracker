import StorageService from './storageService.js';

class FoodService {
  constructor() {
    this.foodLog = [];
  }

  loadFoodLog() {
    this.foodLog = StorageService.loadFoodLog();
    return this.foodLog;
  }

  addFood(food) {
    if (!this.validateFood(food)) {
      throw new Error('Invalid food data');
    }

    this.foodLog.push(food);
    StorageService.saveFoodLog(this.foodLog);
    return this.foodLog;
  }

  clearFoodLog() {
    this.foodLog = [];
    StorageService.clearFoodLog();
    return this.foodLog;
  }

  calculateTotals() {
    return this.foodLog.reduce((totals, food) => {
      totals.calories += Number(food.calories) || 0;
      totals.protein += Number(food.protein) || 0;
      totals.carbs += Number(food.carbs) || 0;
      totals.fat += Number(food.fat) || 0;
      return totals;
    }, { calories: 0, protein: 0, carbs: 0, fat: 0 });
  }

  validateFood(food) {
    if (!food.name || typeof food.name !== 'string') {
      return false;
    }

    const requiredFields = ['calories', 'protein', 'carbs', 'fat'];
    for (const field of requiredFields) {
      const value = Number(food[field]);
      if (isNaN(value) || value < 0) {
        return false;
      }
    }

    if (food.quantity !== null && food.quantity !== undefined) {
      const quantity = Number(food.quantity);
      if (isNaN(quantity) || quantity <= 0) {
        return false;
      }
    }

    return true;
  }

  calculateNutrientsForQuantity(nutrients, quantity) {
    const scale = quantity / 100;
    return {
      calories: (nutrients.calories || 0) * scale,
      protein: (nutrients.protein || 0) * scale,
      carbs: (nutrients.carbs || 0) * scale,
      fat: (nutrients.fat || 0) * scale
    };
  }
}

export default FoodService; 