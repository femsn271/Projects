import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load the BankLoan training dataset
train_df = pd.read_csv('BANK LOAN.csv')

# 2 & 3. Define target variable (Defaulter) and features (all except SN)
# Handles potential column variations (Defaulter / DEFAULTE)
target_col = 'DEFAULTER'
X_train = train_df.drop(columns=['SN', target_col], errors='ignore')
y_train = train_df[target_col]

# 4. Develop Random Forest classification model with 500 trees
rf_model = RandomForestClassifier(n_estimators=500, random_state=42)
rf_model.fit(X_train, y_train)

# Save model artifact and expected feature list
joblib.dump(rf_model, 'rf_bank_model.pkl')
joblib.dump(X_train.columns.tolist(), 'model_features.pkl')

# 5. Load BankLoan_Test dataset and estimate probability of default
test_df = pd.read_csv('BANK_LOAN_TEST.csv')
X_test = test_df.drop(columns=['SN', target_col], errors='ignore')

# Estimate probability for class 1 (Default)
test_df['Predicted_Default_Probability'] = rf_model.predict_proba(X_test)[:, 1]
#test_df.to_csv('BANK_LOAN_TEST_Predictions.csv', index=False)

print("Model training complete. Model artifacts saved.")