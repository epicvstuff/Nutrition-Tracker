import aiohttp
from loguru import logger
from typing import List, Dict, Optional
from ..config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.session: Optional[aiohttp.ClientSession] = None
        
        self.system_prompt = """You are a friendly and knowledgeable nutrition expert assistant. Your role is to:

1. Help users track their food intake by providing accurate nutritional information
2. When a user describes food they're eating, provide estimates for:
   - Calories (kcal)
   - Protein (g)
   - Carbohydrates (g)
   - Fat (g)
3. Ask clarifying questions if needed (portion size, preparation method, specific ingredients)
4. Provide reasonable estimates when exact data isn't available
5. Be encouraging and supportive about healthy eating habits

IMPORTANT: When you provide nutritional information for a food item, you MUST include a special data tag at the END of your response so the user can easily add it to their food log. Use this exact format:

<!--NUTRITION_DATA:{"name":"food name","calories":123,"protein":5.0,"carbs":20.0,"fat":8.0}-->

The values should be numbers (not strings). Use your best estimate based on typical serving sizes.

Example response:
"A medium banana (about 118g) contains approximately:
- Calories: 105 kcal
- Protein: 1.3g
- Carbs: 27g
- Fat: 0.4g

Great choice for a quick energy boost!

<!--NUTRITION_DATA:{"name":"Medium Banana","calories":105,"protein":1.3,"carbs":27,"fat":0.4}-->"

Always include the NUTRITION_DATA tag when you provide specific nutritional numbers. Do NOT include the tag when asking clarifying questions.

Be conversational but concise. Focus on being helpful for nutrition tracking."""

    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def chat(self, message: str, conversation_history: List[Dict] = None) -> str:
        """Send a message to Gemini and get a response."""
        if not self.api_key:
            logger.warning("Gemini API key not configured")
            return "I'm sorry, the AI assistant is not configured. Please add a Gemini API key."

        try:
            session = await self.get_session()
            
            # Build the conversation contents
            contents = []
            
            # Add system prompt as first user message
            contents.append({
                "role": "user",
                "parts": [{"text": f"[System Instructions]: {self.system_prompt}"}]
            })
            contents.append({
                "role": "model", 
                "parts": [{"text": "Understood! I'm ready to help you with nutrition tracking. What would you like to know about?"}]
            })
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })
            
            # Add current message
            contents.append({
                "role": "user",
                "parts": [{"text": message}]
            })
            
            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Gemini API error: {response.status} - {error_text}")
                    return "I'm having trouble connecting right now. Please try again."
                
                data = await response.json()
                
                # Extract the response text
                candidates = data.get("candidates", [])
                if candidates and candidates[0].get("content", {}).get("parts"):
                    return candidates[0]["content"]["parts"][0]["text"]
                else:
                    logger.warning(f"Unexpected Gemini response format: {data}")
                    return "I couldn't generate a response. Please try again."
                    
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return f"Sorry, I encountered an error. Please try again."

gemini_service = GeminiService()

