from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


# Define input schema for request body
class InputData(BaseModel):
    area: float  # This should match your training feature


# Load the trained model (from local .pkl)
model = joblib.load("model.pkl")  # Make sure the path is correct


# Initialize FastAPI app
app = FastAPI(title="Housing Price Predictor API")


# Define /predict endpoint
@app.post("/predict")
def predict(data: InputData):
    # Convert input to DataFrame for model
    df = pd.DataFrame([data.dict()])

    # Make prediction
    prediction = model.predict(df)

    # Return as JSON
    return {"prediction": prediction.tolist()}
