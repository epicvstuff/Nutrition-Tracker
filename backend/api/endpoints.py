from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from PIL import Image
import io
from loguru import logger
from typing import List, Optional

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

@router.get("/search-foods")
async def search_foods(
    query: str = Query(..., description="Food name to search for"),
    limit: int = Query(10, description="Maximum number of results to return", ge=1, le=50)
):
    """Search for multiple food items in USDA database."""
    try:
        logger.info(f"Searching USDA database for foods: {query} (limit: {limit})")
        
        # Search USDA database for multiple foods
        search_results = await usda_service.search_foods(query, limit)
        
        if not search_results:
            logger.warning(f"No foods found for query: {query}")
            return JSONResponse(content={
                "query": query,
                "results": [],
                "message": "No foods found in USDA database"
            })
        
        # Format results for frontend
        formatted_results = []
        for food_item in search_results:
            try:
                # Get FDC ID from the correct field (fdcId in USDA response)
                fdc_id = food_item.get("fdcId") or food_item.get("fdc_id")
                if not fdc_id:
                    logger.warning(f"No FDC ID found for food item: {food_item}")
                    continue
                
                # Get detailed nutrition info for each food
                food_details = await usda_service.get_food_details(str(fdc_id))
                if food_details:
                    # Extract nutrition data from the raw food details
                    nutrition_info = usda_service._extract_nutrition_data(food_details, food_item["description"])
                    formatted_results.append({
                        "id": fdc_id,
                        "name": food_item["description"],
                        "data_type": food_item.get("dataType", "Unknown"),
                        "nutrients": {
                            "calories": nutrition_info.get("calories", 0),
                            "protein": nutrition_info.get("protein", 0),
                            "carbs": nutrition_info.get("carbs", 0),
                            "fat": nutrition_info.get("fat", 0),
                            "fiber": nutrition_info.get("fiber", 0),
                            "sugars": nutrition_info.get("sugars", 0),
                            "sodium": nutrition_info.get("sodium", 0)
                        },
                        "serving_size": nutrition_info.get("serving_size", "100g"),
                        "source": "USDA FoodData Central"
                    })
            except Exception as e:
                logger.warning(f"Failed to get details for {food_item['description']}: {str(e)}")
                # Still add basic info even if detailed nutrition fails
                formatted_results.append({
                    "id": fdc_id,
                    "name": food_item["description"],
                    "data_type": food_item.get("dataType", "Unknown"),
                    "nutrients": {
                        "calories": 0,
                        "protein": 0,
                        "carbs": 0,
                        "fat": 0,
                        "fiber": 0,
                        "sugars": 0,
                        "sodium": 0
                    },
                    "serving_size": "100g",
                    "source": "USDA FoodData Central"
                })
        
        response = {
            "query": query,
            "results": formatted_results,
            "total_found": len(formatted_results)
        }
        
        logger.info(f"Successfully found {len(formatted_results)} foods for query: {query}")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error searching foods: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching foods: {str(e)}"
        ) 