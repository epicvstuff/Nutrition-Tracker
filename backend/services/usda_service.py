import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from loguru import logger
from ..config import settings

class USDAService:
    """Service for fetching nutritional data from USDA FoodData Central API"""
    
    def __init__(self):
        self.api_key = settings.USDA_API_KEY
        self.base_url = settings.USDA_BASE_URL
        self.session = None
        
        # Mapping from model class names to better USDA search terms
        self.food_name_mapping = {
            "sweetcorn": "sweet corn",
            "jalepeno": "jalapeño peppers",
            "chilli pepper": "hot peppers",
            "bell pepper": "bell peppers",
            "capsicum": "bell peppers", 
            "beetroot": "beets",
            "raddish": "radishes",
            "sweetpotato": "sweet potato",
            "soy beans": "soybeans",
            "peas": "green peas"
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def search_food(self, food_name: str, page_size: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Search for food items in USDA database
        
        Args:
            food_name: Name of the food to search for
            page_size: Number of results to return (default: 5)
            
        Returns:
            List of food items or None if error
        """
        if not self.api_key:
            logger.warning("USDA API key not configured, skipping food search")
            return None
            
        try:
            session = await self._get_session()
            
            # USDA FoodData Central search endpoint
            url = f"{self.base_url}/foods/search"
            params = {
                "api_key": self.api_key,
                "query": food_name,
                "pageSize": page_size,
                "dataType": ["Foundation", "SR Legacy"],  # Focus on high-quality data
                "sortBy": "dataType.keyword",
                "sortOrder": "asc"
            }
            
            logger.info(f"Searching USDA database for: {food_name}")
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    foods = data.get("foods", [])
                    logger.info(f"Found {len(foods)} food items for '{food_name}'")
                    return foods
                else:
                    logger.error(f"USDA API error: {response.status} - {await response.text()}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error searching USDA database: {str(e)}")
            return None
    
    async def search_foods(self, food_name: str, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Search for multiple food items in USDA database (alias for search_food with different limit)
        
        Args:
            food_name: Name of the food to search for
            limit: Number of results to return (default: 10)
            
        Returns:
            List of food items or None if error
        """
        return await self.search_food(food_name, limit)

    async def get_food_details(self, fdc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed nutritional information for a specific food item
        
        Args:
            fdc_id: FDC ID of the food item
            
        Returns:
            Detailed food information or None if error
        """
        if not self.api_key:
            logger.warning("USDA API key not configured, skipping food details")
            return None
            
        try:
            session = await self._get_session()
            
            url = f"{self.base_url}/food/{fdc_id}"
            params = {
                "api_key": self.api_key,
                "format": "abridged"  # Get essential nutrition info
            }
            
            logger.info(f"Fetching details for FDC ID: {fdc_id}")
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Retrieved details for food: {data.get('description', 'Unknown')}")
                    return data
                else:
                    logger.error(f"USDA API error: {response.status} - {await response.text()}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching food details: {str(e)}")
            return None
    
    async def get_nutrition_by_name(self, food_name: str) -> Optional[Dict[str, Any]]:
        """
        Get nutritional information for a food by name
        
        Args:
            food_name: Name of the food
            
        Returns:
            Standardized nutrition information or None if not found
        """
        # Use mapped name if available, otherwise use original name
        search_term = self.food_name_mapping.get(food_name.lower(), food_name)
        
        # Search for the food first
        search_results = await self.search_food(search_term)
        
        if not search_results:
            logger.warning(f"No USDA data found for '{food_name}'")
            return None
        
        # Get the best match (first result, usually most relevant)
        best_match = search_results[0]
        fdc_id = best_match.get("fdcId")
        
        if not fdc_id:
            logger.error("No FDC ID found in search results")
            return None
        
        # Get detailed nutrition info
        food_details = await self.get_food_details(str(fdc_id))
        
        if not food_details:
            return None
        
        # Extract and standardize nutrition data
        return self._extract_nutrition_data(food_details, food_name)
    
    def _extract_nutrition_data(self, food_details: Dict[str, Any], food_name: str) -> Dict[str, Any]:
        """
        Extract and standardize nutrition data from USDA response
        
        Args:
            food_details: Raw USDA food details
            food_name: Original food name for fallback
            
        Returns:
            Standardized nutrition information
        """
        try:
            nutrients = food_details.get("foodNutrients", [])
            
            # Create a mapping of nutrient numbers to values (per 100g)
            nutrient_map = {}
            for nutrient in nutrients:
                nutrient_number = nutrient.get("number")
                amount = nutrient.get("amount", 0)
                if nutrient_number and amount is not None:
                    nutrient_map[nutrient_number] = amount
            
            # Extract key nutrients (USDA nutrient numbers)
            # Energy: 208 (Energy), 957 (Atwater General), 958 (Atwater Specific)
            # Protein: 203, Total lipid (fat): 204, Carbohydrate: 205
            
            # Try multiple energy fields in order of preference
            calories = (nutrient_map.get("208", 0) or 
                       nutrient_map.get("957", 0) or 
                       nutrient_map.get("958", 0))
            
            protein = nutrient_map.get("203", 0)      # g per 100g
            fat = nutrient_map.get("204", 0)          # g per 100g
            carbs = nutrient_map.get("205", 0)        # g per 100g
            
            # Additional nutrients
            fiber = nutrient_map.get("291", 0)        # Fiber, total dietary
            sugars = nutrient_map.get("269.3", 0)     # Sugars, Total
            sodium = nutrient_map.get("307", 0)       # Sodium, Na (mg)
            
            nutrition_data = {
                "name": food_name,
                "description": food_details.get("description", food_name),
                "calories": round(calories, 1),
                "protein": round(protein, 1),
                "carbs": round(carbs, 1),
                "fat": round(fat, 1),
                "fiber": round(fiber, 1),
                "sugars": round(sugars, 1),
                "sodium": round(sodium, 1),
                "source": "USDA FoodData Central",
                "fdc_id": food_details.get("fdcId"),
                "data_type": food_details.get("dataType"),
                "serving_size": "100g"  # USDA data is per 100g
            }
            
            logger.info(f"Extracted nutrition data for '{food_name}': {calories} kcal, {protein}g protein")
            return nutrition_data
            
        except Exception as e:
            logger.error(f"Error extracting nutrition data: {str(e)}")
            # Return basic fallback data
            return {
                "name": food_name,
                "calories": 100,
                "protein": 2.0,
                "carbs": 20.0,
                "fat": 0.5,
                "source": "fallback"
            }

# Global instance
usda_service = USDAService() 