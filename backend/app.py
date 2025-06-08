import io
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from tensorflow.keras.models import load_model
from PIL import Image

# Create a FastAPI instance
app = FastAPI()

# Attempt to load the trained CNN model
try:
    model = load_model("fruit_vegetable_classifier.h5")
    print("Model loaded successfully.")
except Exception as e:
    raise RuntimeError("Failed to load the trained model: " + str(e))

# Specify the input image dimensions (should match your training configuration)
IMG_WIDTH, IMG_HEIGHT = 150, 150

# Define class labels according to the specified classes and their order
class_labels = {
    0: "apple",
    1: "banana",
    2: "beetroot",
    3: "bell pepper",
    4: "cabbage",
    5: "capsicum",
    6: "carrot",
    7: "cauliflower",
    8: "chilli pepper",
    9: "corn",
    10: "cucumber",
    11: "eggplant",
    12: "garlic",
    13: "ginger",
    14: "grapes",
    15: "jalepeno",
    16: "kiwi",
    17: "lemon",
    18: "lettuce",
    19: "mango",
    20: "onion",
    21: "orange",
    22: "paprika",
    23: "pear",
    24: "peas",
    25: "pineapple",
    26: "pomegranate",
    27: "potato",
    28: "raddish",
    29: "soy beans",
    30: "spinach",
    31: "sweetcorn",
    32: "sweetpotato",
    33: "tomato",
    34: "turnip",
    35: "watermelon"
}

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    # Verify the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    try:
        # Read and open the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error processing image: " + str(e))
    
    # Preprocess the image: resize, convert to a normalized array, and add batch dimension
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    
    # Predict the class probabilities using the loaded model
    prediction = model.predict(image_array)
    predicted_index = int(np.argmax(prediction[0]))
    confidence = float(np.max(prediction[0]))
    predicted_class = class_labels.get(predicted_index, "Unknown")
    
    # Return the result as JSON
    return {
        "filename": file.filename,
        "predicted_class": predicted_class,
        "confidence": confidence
    }

# (Optional) Serve an HTML page for testing the classification endpoint
@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Food Item Recognition Demo</title>
  </head>
  <body>
    <h1>Food Item Recognition Demo</h1>
    <form id="uploadForm" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*" required>
      <button type="submit">Upload and Classify</button>
    </form>
    <h2>Results:</h2>
    <pre id="results"></pre>

    <script>
      // When the form is submitted, prevent the default page reload and use fetch to send the image.
      document.getElementById("uploadForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch("/classify", {
          method: "POST",
          body: formData
        })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok, status: ' + response.status);
            }
            return response.json();
          })
          .then(data => {
            document.getElementById("results").textContent = JSON.stringify(data, null, 2);
          })
          .catch(err => {
            document.getElementById("results").textContent = "Error: " + err;
          });
      });
    </script>
  </body>
</html>




    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    # Launch the application using Uvicorn
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
