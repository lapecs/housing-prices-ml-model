import datetime
import io
from typing import List

import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Set experiment name
mlflow.set_experiment("Housing Price Prediction")

# Load the trained model from MLflow
MODEL_URI = "models:/housing_price_prediction_models@champion"  # Replace with your model name and alias
model = mlflow.pyfunc.load_model(MODEL_URI)


# Define the expected input schema for a single prediction
class HouseFeatures(BaseModel):
    bedrooms: float
    bathrooms: float
    sqft_living: float
    sqft_lot: float
    floors: float
    waterfront: float
    view: float
    condition: float
    grade: float
    sqft_above: float
    sqft_basement: float
    yr_built: float
    yr_renovated: float
    zipcode: float
    lat: float
    long: float
    sqft_living15: float
    sqft_lot15: float

@app.post("/predict_single")
def predict_single(features: HouseFeatures):
    """Endpoint for real-time predictions with a single input"""
    
    # Convert input to DataFrame
    df = pd.DataFrame([features.dict()])

    try:

        # Make a prediction
        predicted_price = model.predict(df)

        return {"predicted_price": predicted_price[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...)):
    """Endpoint for batch predictions using a CSV file."""
    try:
        # Read the uploaded CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        # Validate required columns
        required_features = [
            "bedrooms",
            "bathrooms",
            "sqft_living",
            "sqft_lot",
            "floors",
            "waterfront",
            "view",
            "condition",
            "grade",
            "sqft_above",
            "sqft_basement",
            "yr_built",
            "yr_renovated",
            "zipcode",
            "lat",
            "long",
            "sqft_living15",
            "sqft_lot15"
        ]
        if not all(feature in df.columns for feature in required_features):
            missing_cols = set(required_features) - set(df.columns)
            raise HTTPException(
                status_code=400, detail=f"Missing columns: {missing_cols}"
            )

        # Make batch predictions
        predicted_price = model.predict(df)
        # return {"predictions": predicted_price}
        return {"predictions": predicted_price.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


