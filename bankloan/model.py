import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import json

# -----------------------------------------------------------------------------
# 1. Logging Configuration
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("training.log"),  # Saves persistent logs to training.log
        logging.StreamHandler()               # Displays live logs in terminal
    ]
)
logger = logging.getLogger("ModelTrainer")


def run_training_pipeline():
    logger.info("==================================================")
    logger.info("Starting Bank Loan Model Training Pipeline")
    logger.info("==================================================")

    # -------------------------------------------------------------------------
    # 2. Load Training Dataset
    # -------------------------------------------------------------------------
    train_file = 'BANK LOAN.csv'
    try:
        train_df = pd.read_csv(train_file)
        logger.info(f"Loaded training data '{train_file}' ({train_df.shape[0]} rows, {train_df.shape[1]} columns)")
    except Exception as e:
        logger.critical(f"Failed to load training file '{train_file}': {str(e)}", exc_info=True)
        return

    # Dynamic target column resolution
    target_candidates = ['DEFAULTER', 'Defaulter', 'DEFAULTE']
    target_col = next((col for col in target_candidates if col in train_df.columns), None)

    if not target_col:
        logger.critical(f"No target column found. Tried candidates: {target_candidates}")
        return

    logger.info(f"Identified target column: '{target_col}'")

    X_train = train_df.drop(columns=['SN', target_col], errors='ignore')
    y_train = train_df[target_col]
    logger.info(f"Feature set initialized with {X_train.shape[1]} variables: {list(X_train.columns)}")

    # -------------------------------------------------------------------------
    # 3. Model Training & Serialization
    # -------------------------------------------------------------------------
    logger.info("Fitting Random Forest Classifier with 500 trees (random_state=42)...")
    rf_model = RandomForestClassifier(n_estimators=500, random_state=42, min_samples_leaf=5, max_depth=10)
    rf_model.fit(X_train, y_train)
    logger.info("Random Forest training completed successfully.")

    # Model evaluation on training set
    train_preds = rf_model.predict(X_train)
    train_acc = accuracy_score(y_train, train_preds)
    logger.info(f"Training Set Accuracy: {train_acc:.2%}")
    
    # Save metrics
    metrics = {
    "model_type": "Random Forest Classifier",
    "n_estimators": 500,
    "accuracy": float(train_acc)
    }
    with open("model_metrics.json", "w") as f:
        json.dump(metrics, f)

    # Save model artifacts
    try:
        joblib.dump(rf_model, 'rf_bank_model.pkl')
        joblib.dump(X_train.columns.tolist(), 'model_features.pkl')
        logger.info("Saved model artifacts: 'rf_bank_model.pkl' and 'model_features.pkl'")
    except Exception as e:
        logger.error(f"Failed to save model artifacts: {str(e)}", exc_info=True)

    # -------------------------------------------------------------------------
    # 4. Test Dataset Predictions
    # -------------------------------------------------------------------------
    test_file = 'BANK_LOAN_TEST.csv'
    try:
        test_df = pd.read_csv(test_file)
        logger.info(f"Loaded test data '{test_file}' ({test_df.shape[0]} rows)")

        X_test = test_df.drop(columns=['SN', target_col], errors='ignore')
        # Reindex test features to guarantee identical column structure as training
        X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

        # Estimate probabilities
        test_df['Predicted_Default_Probability'] = rf_model.predict_proba(X_test)[:, 1]
        
        output_csv = 'BANK_LOAN_TEST_Predictions.csv'
        test_df.to_csv(output_csv, index=False)
        logger.info(f"Saved test predictions to '{output_csv}'")

    except Exception as e:
        logger.error(f"Error processing test dataset '{test_file}': {str(e)}", exc_info=True)
        return

    # -------------------------------------------------------------------------
    # 5. Data Drift Detection
    # -------------------------------------------------------------------------
    threshold = 0.10  # 10% drift threshold
    logger.info(f"Running Data Drift Detection (Threshold: {threshold:.0%})...")

    drift_found = False
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        train_mean = X_train[col].mean()
        test_mean = X_test[col].mean()

        if train_mean != 0:
            pct_change = abs(train_mean - test_mean) / abs(train_mean)
            if pct_change > threshold:
                drift_found = True
                logger.warning(
                    f"Data Drift Detected in '{col}'! "
                    f"Train Mean: {train_mean:.2f} -> Test Mean: {test_mean:.2f} "
                    f"(Shift: {pct_change:.1%})"
                )

    if not drift_found:
        logger.info("No significant data drift detected across numeric features.")

    logger.info("Pipeline execution complete.")


if __name__ == "__main__":
    run_training_pipeline()

