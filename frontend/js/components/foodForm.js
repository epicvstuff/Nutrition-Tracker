class FoodFormComponent {
  constructor(onAddFood) {
    this.onAddFood = onAddFood;
    this.foodForm = document.getElementById('food-form');
    this.foodNameInput = document.getElementById('food-name');
    this.quantityInput = document.getElementById('quantity');
    this.caloriesInput = document.getElementById('calories');
    this.proteinInput = document.getElementById('protein');
    this.carbsInput = document.getElementById('carbs');
    this.fatInput = document.getElementById('fat');
    this.clearSelectionButton = document.getElementById('clear-selection-button');
    
    this.isManualMode = true;
    this.selectedFoodNutrients = null;
    
    this.bindEvents();
    this.updateFormMode();
  }

  bindEvents() {
    this.foodForm.addEventListener('submit', this.handleSubmit.bind(this));
    this.clearSelectionButton.addEventListener('click', this.clearSelection.bind(this));
  }

  setSelectedFood(food) {
    this.selectedFoodNutrients = food.nutrients;
    this.foodNameInput.value = food.name;
    this.isManualMode = false;
    this.updateFormMode();
  }

  clearSelection() {
    this.selectedFoodNutrients = null;
    this.isManualMode = true;
    this.foodNameInput.value = '';
    this.foodNameInput.focus();
    this.updateFormMode();
  }

  updateFormMode() {
    if (this.isManualMode) {
      this.foodNameInput.readOnly = false;
      this.foodNameInput.placeholder = "Type food name";

      this.quantityInput.disabled = true;
      this.quantityInput.value = '';
      this.quantityInput.required = false;

      this.caloriesInput.disabled = false;
      this.proteinInput.disabled = false;
      this.carbsInput.disabled = false;
      this.fatInput.disabled = false;

      this.caloriesInput.required = true;
      this.proteinInput.required = true;
      this.carbsInput.required = true;
      this.fatInput.required = true;

      this.clearSelectionButton.style.display = 'none';
    } else {
      this.foodNameInput.readOnly = true;
      this.foodNameInput.placeholder = "Select food from search";

      this.quantityInput.disabled = false;
      this.quantityInput.required = true;

      this.caloriesInput.disabled = true;
      this.proteinInput.disabled = true;
      this.carbsInput.disabled = true;
      this.fatInput.disabled = true;

      this.caloriesInput.value = '';
      this.proteinInput.value = '';
      this.carbsInput.value = '';
      this.fatInput.value = '';

      this.caloriesInput.required = false;
      this.proteinInput.required = false;
      this.carbsInput.required = false;
      this.fatInput.required = false;

      this.clearSelectionButton.style.display = 'inline-block';
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    let foodToAdd = null;

    if (this.isManualMode) {
      foodToAdd = this.getManualFoodData();
    } else {
      foodToAdd = this.getSelectedFoodData();
    }

    if (foodToAdd) {
      this.onAddFood(foodToAdd);
      this.foodForm.reset();
      this.clearSelection();
    }
  }

  getManualFoodData() {
    const foodName = this.foodNameInput.value.trim();
    const calories = parseFloat(this.caloriesInput.value);
    const protein = parseFloat(this.proteinInput.value);
    const carbs = parseFloat(this.carbsInput.value);
    const fat = parseFloat(this.fatInput.value);

    if (!foodName) {
      alert("Please enter a food name.");
      this.foodNameInput.focus();
      return null;
    }

    if (isNaN(calories) || isNaN(protein) || isNaN(carbs) || isNaN(fat)) {
      alert("Please enter valid numbers for all nutrients (Calories, Protein, Carbs, Fat).");
      return null;
    }

    if (calories < 0 || protein < 0 || carbs < 0 || fat < 0) {
      alert("Nutrient values cannot be negative.");
      return null;
    }

    return {
      name: foodName,
      quantity: null,
      calories,
      protein,
      carbs,
      fat
    };
  }

  getSelectedFoodData() {
    if (!this.selectedFoodNutrients) {
      alert("Internal error: No food selected but not in manual mode. Please clear selection or select a food.");
      return null;
    }

    const quantity = parseFloat(this.quantityInput.value);
    if (isNaN(quantity) || quantity <= 0) {
      alert("Please enter a valid quantity (greater than 0) for the selected food.");
      this.quantityInput.focus();
      return null;
    }

    const scale = quantity / 100;
    return {
      name: this.foodNameInput.value,
      quantity,
      calories: (this.selectedFoodNutrients.calories || 0) * scale,
      protein: (this.selectedFoodNutrients.protein || 0) * scale,
      carbs: (this.selectedFoodNutrients.carbs || 0) * scale,
      fat: (this.selectedFoodNutrients.fat || 0) * scale
    };
  }
}

export default FoodFormComponent; 