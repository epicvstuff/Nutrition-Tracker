from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import numpy as np
from PIL import Image

class BaseModel(ABC):
    """Base class for all food classification models."""
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the model from disk."""
        pass
    
    @abstractmethod
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess the image for model input."""
        pass
    
    @abstractmethod
    def predict(self, image: Image.Image) -> Tuple[str, float]:
        """Make a prediction on the input image.
        
        Returns:
            Tuple[str, float]: (predicted_class, confidence)
        """
        pass
    
    @abstractmethod
    def get_nutritional_info(self, food_class: str) -> Dict[str, Any]:
        """Get nutritional information for the predicted food class.
        
        Returns:
            Dict[str, Any]: Dictionary containing nutritional information
        """
        pass 