class StorageService {
  static STORAGE_KEY = 'foodLogData';

  static saveFoodLog(foodLog) {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(foodLog));
      return true;
    } catch (error) {
      console.error('StorageService.saveFoodLog error:', error);
      return false;
    }
  }

  static loadFoodLog() {
    try {
      const savedData = localStorage.getItem(this.STORAGE_KEY);
      return savedData ? JSON.parse(savedData) : [];
    } catch (error) {
      console.error('StorageService.loadFoodLog error:', error);
      return [];
    }
  }

  static clearFoodLog() {
    try {
      localStorage.removeItem(this.STORAGE_KEY);
      return true;
    } catch (error) {
      console.error('StorageService.clearFoodLog error:', error);
      return false;
    }
  }
}

export default StorageService; 