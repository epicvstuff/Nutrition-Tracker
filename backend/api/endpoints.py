from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from loguru import logger

from ..models.cnn_model import CNNModel
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
        
        # Get nutritional information
        nutrition_info = model.get_nutritional_info(predicted_class)
        logger.info(f"Nutrition info retrieved: {nutrition_info}")
        
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