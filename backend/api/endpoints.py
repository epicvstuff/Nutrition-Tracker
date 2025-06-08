from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from loguru import logger

from ..models.cnn_model import CNNModel
from ..services.usda_service import usda_service
from ..config import settings

router = APIRouter()
model = CNNModel()

@router.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    """Classify a food image and return nutritional information."""
    try:
        logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # Verify file type
        if not file.content_type.startswith("image/"):
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image."
            )
        
        # Read and process image
        contents = await file.read()
        logger.info(f"Read {len(contents)} bytes from file")
        
        try:
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            logger.info(f"Successfully opened image: {image.size}")
        except Exception as e:
            logger.error(f"Failed to open image: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to process image: {str(e)}"
            )
        
        # Get prediction
        try:
            predicted_class, confidence = model.predict(image)
            logger.info(f"Prediction successful: {predicted_class} ({confidence})")
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to classify image: {str(e)}"
            )
        
        # Get nutritional information from USDA API
        try:
            nutrition_info = await usda_service.get_nutrition_by_name(predicted_class)
            
            # If USDA data not available, fall back to model's basic info
            if nutrition_info is None:
                logger.warning(f"USDA data not available for '{predicted_class}', using fallback")
                nutrition_info = model.get_nutritional_info(predicted_class)
                nutrition_info["source"] = "fallback"
            
            logger.info(f"Nutrition info retrieved: {nutrition_info}")
            
        except Exception as e:
            logger.error(f"Error fetching nutrition data: {str(e)}")
            # Fall back to basic model data
            nutrition_info = model.get_nutritional_info(predicted_class)
            nutrition_info["source"] = "fallback"
        
        # Prepare response
        response = {
            "filename": file.filename,
            "predicted_class": predicted_class,
            "confidence": confidence,
            "nutrition_info": nutrition_info
        }
        
        logger.info(f"Successfully classified image: {file.filename}")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

@router.get("/search-nutrition/{food_name}")
async def search_nutrition(food_name: str):
    """Search for nutritional information of a specific food item."""
    try:
        logger.info(f"Searching nutrition data for: {food_name}")
        
        # Get nutritional information from USDA API
        nutrition_info = await usda_service.get_nutrition_by_name(food_name)
        
        if nutrition_info is None:
            logger.warning(f"No nutrition data found for '{food_name}'")
            raise HTTPException(
                status_code=404,
                detail=f"No nutritional data found for '{food_name}'"
            )
        
        logger.info(f"Successfully retrieved nutrition data for: {food_name}")
        return JSONResponse(content=nutrition_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching nutrition data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching nutrition data: {str(e)}"
        ) 