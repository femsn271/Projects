# Bank Loan Default Prediction

A machine learning project developed to predict the probability of loan default using a Random Forest classifier. The project combines a Python machine learning pipeline, a FastAPI prediction API, and an Excel/VBA interface.

The project was developed as an early machine learning module project and demonstrates the workflow from data preparation and model training to API deployment and user interaction through Excel.

## Live Application

**Download Excel file**

https://drive.google.com/file/d/1VSj886B3dptvjcH4ce3Jkhv4zhqVve1n/view?usp=drive_link

**API deployed on Render:**

https://bank-defaulters-predict.onrender.com

---

## Project Overview

The objective of this project is to predict whether a bank loan applicant is likely to default based on financial and demographic information.

The project demonstrates:

- Data loading and preprocessing
- Feature selection
- Random Forest classification
- Model serialization with Joblib
- Prediction probability generation
- FastAPI REST API development
- Excel/VBA integration
- Basic data distribution monitoring
- Logging
- Cloud deployment using Render

### Workflow

Bank Loan Dataset
        │
        ▼
Data Preparation
        │
        ▼
Random Forest Classifier
        │
        ├── Model Metrics
        │
        ├── Saved Model
        │
        ▼
FastAPI REST API
        │
        ▼
Excel / VBA Interface

### Dataset
The model uses financial and demographic information related to loan applicants.
Features
Feature	Description
AGE	Applicant age
EMPLOY	Employment information
ADDRESS	Address-related information
DEBTINC	Debt-to-income information
CREDDEBT	Credit debt
OTHDEBT	Other debt
DEFAULTER	Target variable
SN	Record identifier


SN is treated as an identifier and is not used as a model feature.
The training pipeline uses the following predictive variables:
AGE
EMPLOY
ADDRESS
DEBTINC
CREDDEBT
OTHDEBT

Target:
DEFAULTER

## Machine Learning Model
The project uses a Random Forest Classifier from Scikit-learn.
### Model Configuration
Algorithm: Random Forest Classifier
Number of trees: 500
Maximum depth: 10
Minimum samples per leaf: 5
Random state: 42

The model is trained using the project's bank loan training dataset.

### Training Metric
The current model artifact records:
Training accuracy: 89.43%

This value represents performance on the training data and should not be interpreted as independent test-set accuracy.
The project does not currently use a dedicated independently evaluated test metric as the primary reported model performance.

### Model Artifacts
The trained model is saved using Joblib.
rf_bank_model.pkl
model_features.pkl
model_metrics.json

The metrics file records the model type, number of estimators, and training accuracy.
Example:
{
  "model_type": "Random Forest Classifier",
  "n_estimators": 500,
  "training_accuracy": 0.8942857142857142
}

## FastAPI
The trained model is exposed through a REST API built with FastAPI.

### Available Endpoints
#### Health Check
GET /health

Used to verify that the API is running.

#### Prediction
POST /predict

Receives applicant information and returns a prediction from the trained model.
Example request structure:
{
  "AGE": 35,
  "EMPLOY": 10,
  "ADDRESS": 5,
  "DEBTINC": 20.5,
  "CREDDEBT": 2.5,
  "OTHDEBT": 1.8
}

#### Metadata
GET /metadata

Returns information about the deployed model and its configuration.


## Excel / VBA Integration
One of the practical components of the project is integration with Microsoft Excel.
The Excel workbook uses VBA to send applicant information to the deployed FastAPI endpoint.
Excel
  │
  │ VBA HTTP Request
  ▼
FastAPI /predict
  │
  ▼
Random Forest Model
  │
  ▼
Prediction
  │
  ▼
Excel

This allows the machine learning model to be used through a familiar spreadsheet interface without requiring the user to run Python directly.

## Basic Data Monitoring
The training pipeline includes a simple feature-distribution monitoring step.
The implementation compares the mean of numeric features between the training dataset and the prediction/test dataset.
A 10% relative mean shift is used as the current threshold for flagging potential distribution changes.
This is a basic monitoring approach rather than a full statistical drift-detection framework.
Possible future improvements include:
- Population Stability Index (PSI)
- Kolmogorov-Smirnov testing
- Wasserstein distance
- Evidently
- Automated monitoring dashboards

## Logging
The training pipeline uses Python's logging module to record important events during execution.
Example information includes:
- Dataset loading
- Feature selection
- Model training
- Training performance
- Prediction generation
- Data distribution checks
- Model artifact creation
- Errors and exceptions
Training logs are stored in:
training.log

## Technology Stack
### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest
- Joblib
### API
- FastAPI
- Uvicorn
### User Interface / Integration
- Microsoft Excel
- VBA
### Deployment
- Render
- Gunicorn
### Development
- Git
- GitHub

## Project Structure
bankloan/
│
├── app.py
├── model.py
│
├── BANK LOAN.csv
├── BANK_LOAN_TEST.csv
├── BANK_LOAN_TEST_Predictions.csv
│
├── rf_bank_model.pkl
├── model_features.pkl
├── model_metrics.json
│
├── training.log
├── requirements.txt
│
├── bank_loan_api.xlsm
├── bank_loan_local.xlsm
│
└── README.md

## Running Locally
1. Clone the repository
git clone <your-repository-url>
cd bankloan

2. Create a virtual environment
python -m venv .venv

Activate it on Windows:
.venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Run the API
uvicorn app:app --reload

The API will be available locally at:
http://127.0.0.1:8000

FastAPI documentation is available at:
http://127.0.0.1:8000/docs

## Deployment
The API is deployed using Render.
The deployed service exposes the FastAPI application and allows the Excel/VBA interface to communicate with the machine learning model remotely.


Live API:
https://bank-defaulters-predict.onrender.com


Limitations
This project represents an early machine learning implementation and has several limitations.

### Model Evaluation
The recorded 89.43% accuracy is calculated on the training data. A dedicated independent evaluation should be added before using the model for real-world decision-making.


### Data Drift
The current monitoring implementation uses a simple comparison of numeric feature means. More robust statistical methods would be appropriate for production monitoring.

### Model Explainability
The project does not currently provide detailed explanations for individual predictions.

### Production Considerations
A production implementation would require additional controls such as:
- Authentication and authorization
- Input validation and schema versioning
- More comprehensive model evaluation
- Model version management
- Monitoring and alerting
- Data privacy controls
- Fairness and bias evaluation


## Future Improvements
Potential improvements include:
- Add an independent validation/test evaluation
- Add ROC-AUC, precision, recall and F1-score
- Add confusion matrix analysis
- Improve data-drift monitoring
- Add model explainability with SHAP
- Add API authentication
- Add automated testing
- Add CI/CD
- Add model versioning
- Improve monitoring and observability

## Learning Outcomes
This project provided practical experience with:
- Building a supervised machine learning classification model
- Working with structured financial data
- Training and serializing a Random Forest model
- Creating a REST API with FastAPI
- Connecting a machine learning API to Excel using VBA
- Deploying a Python application to the cloud
- Implementing application logging
- Introducing basic monitoring concepts
It also provided an early foundation for the more advanced machine learning and deployment projects developed later in the portfolio.


## Disclaimer
This project is for educational and demonstration purposes only.
It should not be used to make real-world lending or financial decisions without appropriate validation, governance, security, fairness assessment, and regulatory review.
