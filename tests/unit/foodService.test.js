import { FoodService } from '../../js/services/foodService';

describe('FoodService', () => {
  let foodService;
  const mockFood = {
    id: '1',
    name: 'Apple',
    quantity: 100,
    calories: 52,
    protein: 0.3,
    carbs: 14,
    fat: 0.2,
    date: '2024-03-20'
  };

  beforeEach(() => {
    foodService = new FoodService();
    localStorage.clear();
  });

  describe('addFood', () => {
    test('should add food to the log', () => {
      foodService.addFood(mockFood);
      const foodLog = foodService.getFoodLog();
      expect(foodLog).toHaveLength(1);
      expect(foodLog[0]).toEqual(mockFood);
    });

    test('should validate food data', () => {
      const invalidFood = { ...mockFood, calories: -1 };
      expect(() => foodService.addFood(invalidFood)).toThrow();
    });
  });

  describe('getFoodLog', () => {
    test('should return empty array for new service', () => {
      const foodLog = foodService.getFoodLog();
      expect(foodLog).toHaveLength(0);
    });

    test('should return all food entries', () => {
      foodService.addFood(mockFood);
      const foodLog = foodService.getFoodLog();
      expect(foodLog).toHaveLength(1);
    });
  });

  describe('calculateTotals', () => {
    test('should calculate correct totals', () => {
      foodService.addFood(mockFood);
      const totals = foodService.calculateTotals();
      expect(totals).toEqual({
        calories: 52,
        protein: 0.3,
        carbs: 14,
        fat: 0.2
      });
    });

    test('should return zeros for empty log', () => {
      const totals = foodService.calculateTotals();
      expect(totals).toEqual({
        calories: 0,
        protein: 0,
        carbs: 0,
        fat: 0
      });
    });
  });

  describe('clearFoodLog', () => {
    test('should clear all food entries', () => {
      foodService.addFood(mockFood);
      foodService.clearFoodLog();
      const foodLog = foodService.getFoodLog();
      expect(foodLog).toHaveLength(0);
    });
  });
}); 