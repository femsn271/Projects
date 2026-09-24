# Projects
💳 Credit Default Prediction Dash App

A clean, interactive web application built with Python, Dash, and Plotly for predicting credit defaults using a Logistic Regression model.

The app trains a logistic regression model on server startup using a local training dataset (BANK LOAN.csv), and allows users to upload custom test datasets through a web interface to evaluate default probabilities and adjust classification thresholds dynamically.

✨ Features

Automated Server-Side Training: Automatically trains a Scikit-Learn LogisticRegression model on startup using BANK LOAN.csv.

Interactive CSV Upload: Drag-and-drop or browse interface to upload test datasets (.csv).

Dynamic Threshold Selection: A dropdown control (ranging from 0.1 to 0.9) to instantly recalculate and update defaulter vs. non-defaulter counts and classification boundaries.

Visual Analytics: Interactive probability distribution histogram powered by Plotly, featuring a dynamic threshold reference line.

Data Preview Table: Instant top-10 record preview filtered dynamically based on the chosen threshold.

Modern UI: Styled with dash-bootstrap-components (FLATLY theme) for a clean, professional dashboard appearance.

🛠️ Tech Stack

Python 3.x

Dash & Dash Bootstrap Components (Web Framework & UI)

Pandas & NumPy (Data Processing)

Scikit-Learn (Machine Learning Model)

Plotly (Interactive Data Visualizations)

🚀 Getting Started

Prerequisites

Make sure you have Python installed along with the required libraries. You can install them via pip using requirements.txt


Project Structure

Ensure your project directory contains the application file and the training dataset:

DASH/
│
├── app.py              # Main Dash application
├── BANK LOAN.csv       # Training dataset (Required on startup)
└── README.md           # Project documentation


Running the Application

Open your terminal or PowerShell in the project directory.

Activate your virtual environment (if applicable):

.venv\Scripts\Activate


Run the application script:

python app.py


The application will automatically launch your default web browser and open:
http://127.0.0.1:8050

📌 Usage Guide

Server Startup: The app verifies and trains the model on BANK LOAN.csv. Look for the confirmation message: Model trained successfully on server startup.

Upload Test Data: Use the upload card on the dashboard to upload a test CSV file containing the same feature columns as the training dataset, you can find a test file in the assets folder.

Analyze Probabilities:

View the Probability Distribution plot to see the spread of predicted default risks.

Adjust the Probability Threshold dropdown to filter predictions.

Review the updated Defaulter / Non-Defaulter counts and browse the top preview records in the table.