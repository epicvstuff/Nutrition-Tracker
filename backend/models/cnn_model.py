import numpy as np
from keras.models import load_model
from PIL import Image
from typing import Dict, Any, Tuple
import os

from .base_model import BaseModel
from ..config import settings

class CNNModel(BaseModel):
    def __init__(self):
        self.model = None
        # Default class labels - these will be updated when model loads
        self.class_labels = {
            0: "apple", 1: "banana", 2: "beetroot", 3: "bell pepper",
            4: "cabbage", 5: "capsicum", 6: "carrot", 7: "cauliflower",
            8: "chilli pepper", 9: "corn", 10: "cucumber", 11: "eggplant",
            12: "garlic", 13: "ginger", 14: "grapes", 15: "jalepeno",
            16: "kiwi", 17: "lemon", 18: "lettuce", 19: "mango",
            20: "onion", 21: "orange", 22: "paprika", 23: "pear",
            24: "peas", 25: "pineapple", 26: "pomegranate", 27: "potato",
            28: "raddish", 29: "soy beans", 30: "spinach", 31: "sweetcorn",
            32: "sweetpotato", 33: "tomato", 34: "turnip", 35: "watermelon"
        }
        self.load_model()

    def load_model(self) -> None:
        """Load the CNN model from disk."""
        try:
            if not os.path.exists(settings.MODEL_PATH):
                print(f"Warning: Model file not found at {settings.MODEL_PATH}. Using mock predictions.")
                self.model = None
                return
            self.model = load_model(settings.MODEL_PATH)
            print(f"Successfully loaded model from {settings.MODEL_PATH}")
        except Exception as e:
            print(f"Warning: Failed to load CNN model: {str(e)}. Using mock predictions.")
            self.model = None

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess the image for CNN input."""
        # Resize image
        image = image.resize((settings.IMG_WIDTH, settings.IMG_HEIGHT))
        # Convert to array and normalize (same as training)
        image_array = np.array(image) / 255.0
        # Add batch dimension
        return np.expand_dims(image_array, axis=0)

    def predict(self, image: Image.Image) -> Tuple[str, float]:
        """Make a prediction using the CNN model."""
        if self.model is None:
            # Return a mock prediction when model is not available
            return "apple", 0.95  # Mock prediction
            
        # Preprocess image
        processed_image = self.preprocess_image(image)
        # Get prediction
        prediction = self.model.predict(processed_image, verbose=0)
        predicted_index = int(np.argmax(prediction[0]))
        confidence = float(np.max(prediction[0]))
        predicted_class = self.class_labels.get(predicted_index, f"class_{predicted_index}")
        return predicted_class, confidence

    def get_nutritional_info(self, food_class: str) -> Dict[str, Any]:
        """Get nutritional information for the predicted food class."""
        # This is a placeholder. In a real application, this would query a nutrition database
        # For now, return some default values based on food type
        nutrition_data = {
            "apple": {"calories": 52, "protein": 0.3, "carbs": 14.0, "fat": 0.2},
            "banana": {"calories": 89, "protein": 1.1, "carbs": 23.0, "fat": 0.3},
            "carrot": {"calories": 41, "protein": 0.9, "carbs": 10.0, "fat": 0.2},
            "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
            "orange": {"calories": 47, "protein": 0.9, "carbs": 12.0, "fat": 0.1},
            "grapes": {"calories": 69, "protein": 0.7, "carbs": 16.0, "fat": 0.2},
        }
        
        # Use specific nutrition data if available, otherwise use defaults
        nutrition = nutrition_data.get(food_class, {
            "calories": 100,  # per 100g
            "protein": 2.0,   # per 100g
            "carbs": 20.0,    # per 100g
            "fat": 0.5        # per 100g
        })
        
        return {
            "name": food_class,
            "calories": nutrition["calories"],
            "protein": nutrition["protein"],
            "carbs": nutrition["carbs"],
            "fat": nutrition["fat"]
        } 