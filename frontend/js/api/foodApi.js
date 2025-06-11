const OFF_API_URL = 'https://world.openfoodfacts.org/cgi/search.pl';
const BACKEND_API_URL = 'http://127.0.0.1:8000/api/v1';

class FoodApi {
  /**
   * Search for food items using USDA database first, with OpenFoodFacts as fallback
   * @param {string} query - The search query
   * @param {boolean} useUSDA - Whether to use USDA search (default: true)
   * @returns {Promise<Array>} Array of food items
   */
  static async searchFood(query, useUSDA = true) {
    try {
      // Try USDA search first if available
      if (useUSDA) {
        console.log('Searching USDA database for:', query);
        const usdaResults = await this.searchUSDA(query);
        if (usdaResults && usdaResults.length > 0) {
          console.log(`Found ${usdaResults.length} USDA results for:`, query);
          return usdaResults;
        }
        console.log('No USDA results found, falling back to OpenFoodFacts');
      }
      
      // Fallback to OpenFoodFacts
      console.log('Searching OpenFoodFacts for:', query);
      const offResults = await this.searchOpenFoodFacts(query);
      console.log(`Found ${offResults.length} OpenFoodFacts results for:`, query);
      return offResults;
      
    } catch (error) {
      console.error('FoodApi.searchFood error:', error);
      throw new Error('Failed to search for food items. Please try again.');
    }
  }

  /**
   * Search USDA database via backend API
   * @param {string} query - The search query
   * @returns {Promise<Array>} Array of USDA food items
   */
  static async searchUSDA(query) {
    try {
      const url = `${BACKEND_API_URL}/search-foods?query=${encodeURIComponent(query)}&limit=10`;
      const response = await fetch(url);
      
      if (!response.ok) {
        console.warn(`USDA search failed: ${response.status}`);
        return [];
      }
      
      const data = await response.json();
      return this.processUSDAResults(data.results || []);
      
    } catch (error) {
      console.error('USDA search error:', error);
      return [];
    }
  }

  /**
   * Search OpenFoodFacts database (fallback)
   * @param {string} query - The search query
   * @returns {Promise<Array>} Array of OpenFoodFacts food items
   */
  static async searchOpenFoodFacts(query) {
    try {
      const url = `${OFF_API_URL}?search_terms=${encodeURIComponent(query)}&search_simple=1&action=process&json=1&page_size=20`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return this.processOpenFoodFactsResults(data.products);
      
    } catch (error) {
      console.error('OpenFoodFacts search error:', error);
      throw error;
    }
  }

  /**
   * Process USDA search results into standardized format
   * @param {Array} results - Raw USDA results
   * @returns {Array} Processed food items
   */
  static processUSDAResults(results) {
    if (!results || results.length === 0) {
      return [];
    }

    return results.map(item => ({
      id: item.id,
      name: item.name,
      description: item.name,
      dataType: item.data_type,
      source: 'USDA FoodData Central',
      nutrients: {
        calories: item.nutrients.calories || 0,
        protein: item.nutrients.protein || 0,
        carbs: item.nutrients.carbs || 0,
        fat: item.nutrients.fat || 0,
        fiber: item.nutrients.fiber || 0,
        sugars: item.nutrients.sugars || 0,
        sodium: item.nutrients.sodium || 0
      },
      servingSize: item.serving_size || '100g'
    })).slice(0, 10); // Limit to 10 results
  }

  /**
   * Process OpenFoodFacts search results into standardized format
   * @param {Array} products - Raw OpenFoodFacts products
   * @returns {Array} Processed food items
   */
  static processOpenFoodFactsResults(products) {
    if (!products || products.length === 0) {
      return [];
    }

    return products
      .filter(product => product.nutriments && product.product_name)
      .map(product => ({
        id: product.id || product.code,
        name: product.product_name_en || product.product_name,
        description: product.product_name_en || product.product_name,
        source: 'OpenFoodFacts',
        nutrients: {
          calories: product.nutriments['energy-kcal_100g'] || (product.nutriments['energy_100g'] / 4.184) || 0,
          protein: product.nutriments.proteins_100g || 0,
          carbs: product.nutriments.carbohydrates_100g || 0,
          fat: product.nutriments.fat_100g || 0,
          fiber: product.nutriments.fiber_100g || 0,
          sugars: product.nutriments.sugars_100g || 0,
          sodium: product.nutriments.sodium_100g || 0
        },
        servingSize: '100g'
      }))
      .slice(0, 10); // Limit to 10 results
  }

  /**
   * Get nutrition information for a specific food by name
   * @param {string} foodName - The food name
   * @returns {Promise<Object>} Nutrition information
   */
  static async getNutritionInfo(foodName) {
    try {
      const url = `${BACKEND_API_URL}/search-nutrition/${encodeURIComponent(foodName)}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Nutrition search failed: ${response.status}`);
      }
      
      return await response.json();
      
    } catch (error) {
      console.error('Nutrition info error:', error);
      throw error;
    }
  }
}

export default FoodApi; 