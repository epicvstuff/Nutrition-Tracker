class FoodListComponent {
  constructor() {
    this.foodListTableBody = document.getElementById('food-list');
    this.totalCaloriesEl = document.getElementById('total-calories');
    this.totalProteinEl = document.getElementById('total-protein');
    this.totalCarbsEl = document.getElementById('total-carbs');
    this.totalFatEl = document.getElementById('total-fat');
    this.resetButton = document.getElementById('reset-button');
  }

  renderFoodList(foodLog) {
    this.foodListTableBody.innerHTML = '';
    foodLog.forEach(food => {
      const row = document.createElement('tr');
      const quantityDisplay = (food.quantity === null || food.quantity === undefined) ? '-' : food.quantity.toFixed(0);
      row.innerHTML = `
        <td>${food.name}</td>
        <td>${quantityDisplay}</td>
        <td>${food.calories.toFixed(1)}</td>
        <td>${food.protein.toFixed(1)}</td>
        <td>${food.carbs.toFixed(1)}</td>
        <td>${food.fat.toFixed(1)}</td>
      `;
      this.foodListTableBody.appendChild(row);
    });
  }

  renderTotals(totals) {
    this.totalCaloriesEl.textContent = totals.calories.toFixed(1);
    this.totalProteinEl.textContent = totals.protein.toFixed(1);
    this.totalCarbsEl.textContent = totals.carbs.toFixed(1);
    this.totalFatEl.textContent = totals.fat.toFixed(1);
  }

  setResetHandler(handler) {
    this.resetButton.addEventListener('click', () => {
      if (confirm("Are you sure you want to clear the entire log and start a new day?")) {
        handler();
      }
    });
  }
}

export default FoodListComponent; 