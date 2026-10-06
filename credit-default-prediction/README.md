# Credit Default Prediction Dashboard

An interactive machine learning dashboard for exploring credit default predictions using Logistic Regression and adjustable probability thresholds.

## Live Application

[Credit Default Prediction Dashboard](https://credit-default-prediction-t2pi.onrender.com)

### Download Excel file test/example

https://github.com/femsn271/Projects/blob/main/credit-default-prediction/assets/BANK%20LOAN_TEST.csv

## Overview

This project demonstrates how a machine learning classification model can be integrated into an interactive web application for credit-risk analysis.

The application trains a Logistic Regression model using historical bank-loan data and generates default probabilities for uploaded test records.

Users can adjust the classification threshold and immediately explore how the decision boundary affects the number of predicted defaulters.

## Project Objective

The objective is to provide an interactive interface for exploring credit default predictions rather than simply returning a fixed classification.

The application demonstrates the complete workflow:

1. Load credit data
2. Prepare the model features
3. Train a Logistic Regression classifier
4. Generate default probabilities
5. Apply a user-selected probability threshold
6. Visualize prediction results
7. Inspect records with the highest predicted default probability

## Machine Learning Approach

### Model

The application uses:

- Logistic Regression
- Binary classification
- Probability-based predictions using `predict_proba()`

The model is trained when the application starts.

### Decision Threshold

Instead of relying on a fixed classification threshold, the dashboard allows the user to select a threshold between 0.1 and 0.9.

For example:


Default probability >= selected threshold
                    ↓
              Predicted Default

Changing the threshold changes the number of records classified as potential defaulters.

This demonstrates an important concept in classification: the decision threshold can be adjusted according to the desired balance between different types of classification outcomes.

## Dashboard Features
The dashboard provides:
- CSV upload
- Input validation
- Default probability predictions
- Adjustable classification threshold
- Predicted default/non-default counts
- Probability distribution visualization
- Threshold indicator
- Top 10 highest-risk predictions

## Input Data
The application uses the bank-loan dataset supplied with the project.

The dashboard expects the uploaded test dataset to contain the feature columns required by the trained model.

A sample test file is provided in:
assets/BANK LOAN_TEST.csv

## Application Workflow
Bank Loan Dataset
        │
        ▼
Feature Preparation
        │
        ▼
Logistic Regression
        │
        ▼
Default Probability
        │
        ▼
User-selected Threshold
        │
        ├───────────────┐
        ▼               ▼
    Non-default       Default
        │               │
        └───────┬───────┘
                ▼
       Interactive Dashboard

## Technology Stack

Technology	Purpose
Python	Application and ML development
Pandas	Data loading and processing
NumPy	Numerical operations
Scikit-learn	Logistic Regression
Dash	Interactive web application
Plotly	Data visualization
Dash Bootstrap Components	Dashboard interface
Gunicorn	Production application server
Render	Cloud deployment


## Project Structure
credit-default-prediction/
│
├── assets/
│   ├── BANK LOAN_TEST.csv
│   └── theme.css
│
├── app.py
├── BANK LOAN.csv
├── Procfile
├── requirements.txt
└── README.md

## Running Locally
Create and activate a virtual environment:
python -m venv .venv

Activate it on Windows:
.venv\Scripts\Activate.ps1

Install the dependencies:
pip install -r requirements.txt

Run the application:
python app.py

The Dash application can then be opened in the browser using the local address shown by the application.

## Deployment
The application is deployed using Render with Gunicorn.

The production start command is defined in the Procfile.

## Limitations
This project is primarily an interactive demonstration of machine learning classification and threshold-based decision making.
The current application does not provide a comprehensive model evaluation report containing metrics such as ROC-AUC, precision, recall, or a confusion matrix.
The model is trained when the application starts rather than loaded from a separately persisted model artifact.
The predictions should therefore be considered analytical outputs from the demonstration application rather than production credit decisions.

## Future Improvements
Possible improvements include:
- Persisting the trained model as a model artifact
- Adding cross-validation
- Adding ROC-AUC and precision/recall evaluation
- Adding a confusion matrix
- Comparing multiple classification models
- Adding feature scaling and preprocessing through a reproducible pipeline
- Adding model monitoring
- Improving input validation and error handling
- Separating model training from application serving

## Learning Outcomes
This project demonstrates practical experience with:
- Binary classification
- Logistic Regression
- Probability-based predictions
- Decision-threshold selection
- Interactive machine learning dashboards
- CSV validation
- Data visualization
- Dash application development
- Production deployment with Gunicorn and Render

## Disclaimer
This application is an educational and portfolio project.