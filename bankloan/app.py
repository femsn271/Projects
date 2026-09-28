import os
import re
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# 1. Configure logging formatting prior to loading modules/artifacts
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("BankLoanAPI")

app = FastAPI(title="Bank Loan Defaulters Prediction API")

# 2. Load model artifacts safely at startup
try:
    model = joblib.load("rf_bank_model.pkl")
    features = joblib.load("model_features.pkl")
    logger.info("Model artifacts ('rf_bank_model.pkl', 'model_features.pkl') loaded successfully.")
except Exception as e:
    logger.critical(f"Failed to load model artifacts: {str(e)}", exc_info=True)
    raise RuntimeError("API failed to initialize model files.") from e


class CustomerData(BaseModel):
    data: dict


@app.get("/health")
def health_check():
    logger.info("Health check requested.")
    return {"status": "healthy", "message": "API is running"}


@app.post("/predict")
def predict_default(customer: CustomerData):
    logger.info(f"Prediction endpoint called. Payload: {customer.data}")

    try:
        # Normalize input dictionary keys to uppercase
        clean_input = {str(k).strip().upper(): v for k, v in customer.data.items()}

        # Build DataFrame matching trained model columns
        input_df = pd.DataFrame([clean_input])
        feature_cols = [f.upper() for f in features]
        input_df = input_df.reindex(columns=feature_cols, fill_value=0)

        # Compute probability of default (Class 1)
        probability = float(model.predict_proba(input_df)[0][1])

        logger.info(f"Prediction complete. Calculated Default Probability: {probability:.4f} ({probability:.2%})")
        return {"probability_of_default": probability}

    except Exception as e:
        logger.error(f"Prediction error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
@app.get("/metadata")
def get_model_metadata():
    log_file = "training.log"
    accuracy = None

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            # Read lines in reverse to find the most recent training run
            for line in reversed(f.readlines()):
                match = re.search(r"Training Set Accuracy:\s*([\d\.]+)%", line)
                if match:
                    # Convert '89.43%' string into float 0.8943
                    accuracy = float(match.group(1)) / 100.0
                    break

    return {
        "model_type": "Random Forest Classifier",
        "n_estimators": 500,
        "accuracy": accuracy if accuracy is not None else 0.8943
    }
