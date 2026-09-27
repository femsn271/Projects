Bank Loan Defaulters Prediction System

A full-stack machine learning solution that predicts customer loan default probabilities using a Random Forest model, hosted via a FastAPI REST endpoint, and integrated directly into a Microsoft Excel (.xlsm) user interface.

📁 Repository Structure

Plaintext
├── BankLoan.csv                  # Training dataset
├── BankLoan_Test.csv             # Test dataset
├── train_model.py                # Model training and artifact generation script
├── app.py                        # FastAPI backend application
├── rf_bank_model.pkl             # Serialized Random Forest model (generated)
├── model_features.pkl            # Serialized feature column names (generated)
├── BankLoan_Prediction.xlsm      # Macro-enabled Excel frontend interface
└── README.md                     # Project documentation
