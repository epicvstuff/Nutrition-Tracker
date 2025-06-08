import { FoodFormComponent } from '../../js/components/foodForm';
import { FoodService } from '../../js/services/foodService';

describe('FoodForm Integration', () => {
  let foodForm;
  let foodService;
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    foodService = new FoodService();
    foodForm = new FoodFormComponent(foodService);
    container.innerHTML = `
      <form id="food-form">
        <input type="text" id="food-name" required>
        <input type="number" id="quantity" min="1" step="any">
        <input type="number" id="calories" min="0" step="any">
        <input type="number" id="protein" min="0" step="any">
        <input type="number" id="carbs" min="0" step="any">
        <input type="number" id="fat" min="0" step="any">
        <button type="submit">Add Food</button>
      </form>
    `;
    foodForm.initialize();
  });

  afterEach(() => {
    document.body.removeChild(container);
    localStorage.clear();
  });

  test('should add food to service when form is submitted', () => {
    const form = container.querySelector('#food-form');
    const nameInput = container.querySelector('#food-name');
    const quantityInput = container.querySelector('#quantity');
    const caloriesInput = container.querySelector('#calories');

    nameInput.value = 'Apple';
    quantityInput.value = '100';
    caloriesInput.value = '52';

    form.dispatchEvent(new Event('submit'));

    const foodLog = foodService.getFoodLog();
    expect(foodLog).toHaveLength(1);
    expect(foodLog[0].name).toBe('Apple');
    expect(foodLog[0].quantity).toBe(100);
    expect(foodLog[0].calories).toBe(52);
  });

  test('should validate form inputs', () => {
    const form = container.querySelector('#food-form');
    const nameInput = container.querySelector('#food-name');
    const caloriesInput = container.querySelector('#calories');

    nameInput.value = '';
    caloriesInput.value = '-1';

    form.dispatchEvent(new Event('submit'));

    const foodLog = foodService.getFoodLog();
    expect(foodLog).toHaveLength(0);
  });

  test('should clear form after successful submission', () => {
    const form = container.querySelector('#food-form');
    const nameInput = container.querySelector('#food-name');
    const quantityInput = container.querySelector('#quantity');

    nameInput.value = 'Apple';
    quantityInput.value = '100';

    form.dispatchEvent(new Event('submit'));

    expect(nameInput.value).toBe('');
    expect(quantityInput.value).toBe('');
  });
}); 