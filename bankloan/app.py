from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Bank Loan Defaulters Prediction API")

# -------------------------------------------------
# Health check endpoint
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"message": "API is running"}



# Load model and feature order
model = joblib.load('rf_bank_model.pkl')
features = joblib.load('model_features.pkl')

class CustomerData(BaseModel):
    data: dict

# Task 7: Create FastAPI endpoint (/predict)
@app.post("/predict")
def predict_default(customer: CustomerData):
    # Normalize input dictionary keys to uppercase to prevent case-mismatch issues
    clean_input = {str(k).strip().upper(): v for k, v in customer.data.items()}
    
    # Format into DataFrame matching training feature columns
    input_df = pd.DataFrame([clean_input])
    feature_cols = [f.upper() for f in features]
    input_df = input_df.reindex(columns=feature_cols, fill_value=0)
    
    # Compute probability of default (Class 1)
    probability = model.predict_proba(input_df)[0][1]
    
    return {"probability_of_default": float(probability)}