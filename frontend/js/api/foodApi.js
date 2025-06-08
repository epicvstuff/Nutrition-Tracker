const OFF_API_URL = 'https://world.openfoodfacts.org/cgi/search.pl';

class FoodApi {
  static async searchFood(query) {
    try {
      const url = `${OFF_API_URL}?search_terms=${encodeURIComponent(query)}&search_simple=1&action=process&json=1&page_size=20`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return this.processSearchResults(data.products);
    } catch (error) {
      console.error('FoodApi.searchFood error:', error);
      throw new Error('Failed to search for food items. Please try again.');
    }
  }

  static processSearchResults(products) {
    if (!products || products.length === 0) {
      return [];
    }

    return products
      .filter(product => product.nutriments && product.product_name)
      .map(product => ({
        name: product.product_name_en || product.product_name,
        nutrients: {
          calories: product.nutriments['energy-kcal_100g'] || (product.nutriments['energy_100g'] / 4.184) || 0,
          protein: product.nutriments.proteins_100g || 0,
          carbs: product.nutriments.carbohydrates_100g || 0,
          fat: product.nutriments.fat_100g || 0
        }
      }))
      .slice(0, 10); // Limit to 10 results
  }
}

export default FoodApi; 