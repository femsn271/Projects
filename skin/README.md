Skin Clinic Marketing Campaign Analysis API

Author: Fernanda Machado

Module: M10 PMLS - Assignment 1 (Model Deployment Using FastAPI)

📌 Business Context

A skin clinic conducted a targeted marketing campaign sent to 10,000 customers. The goal of this application is to perform exploratory analysis to identify which customer segments (demographics and purchase behavior) exhibit higher response rates.

These analytical insights serve to optimize future marketing campaign targeting strategies, improve customer engagement, and boost campaign return on investment (ROI).

🎯 Key Metrics & Analysis Performed

The API aggregates customer data and computes the campaign response rate (%) across four primary dimensions:

Gender vs. Campaign Response: Segmented by Female and Male.

Age Group vs. Campaign Response: Categorized into <30, 30–50, and >50.

Purchase in Last Quarter vs. Campaign Response: Segmented by recent purchasing history (Yes / No).

Product Usage vs. Campaign Response: Grouped by the number of unique products purchased in the last year (1–4, 5–8, >8).

🛠️ Technology Stack

Framework: FastAPI

Data Processing: Pandas

ASGI Server: Uvicorn

Frontend / UI: Native HTML & CSS (Dark Mode, Flexbox side-by-side table layout)

📂 Project Structure

.
├── main.py                     # FastAPI application logic & HTML layout
├── skin clinic campaign.csv    # Source campaign dataset
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation


🚀 Local Installation & Execution

Follow these steps to run and test the application on your local machine:

1. Prerequisites

Ensure you have Python 3.8+ installed.

2. Clone / Setup Workspace

Place main.py, skin clinic campaign.csv, and requirements.txt in the same directory.

3. Install Dependencies

Install the required Python packages using pip:

pip install -r requirements.txt


Required packages inside requirements.txt:

fastapi
uvicorn
pandas


4. Run the Application

Start the Uvicorn development server with hot-reloading enabled:

uvicorn main:app --reload


5. Access the Endpoint

Open your web browser and navigate to:

http://127.0.0.1:8000/campaign-analysis


🌐 API Endpoint Specification

GET /campaign-analysis

Description: Computes aggregate campaign response metrics from skin clinic campaign.csv and returns a styled HTML page containing two side-by-side rows of data tables.

Response Type: text/html

Response Output: Dark-themed dashboard with response percentages formatted to 2 decimal places.

☁️ Deployment on Render

To deploy this application to Render:

Push your repository (main.py, requirements.txt, skin clinic campaign.csv, README.md) to GitHub.

Log in to Render and create a new Web Service.

Connect your GitHub repository.

Configure the settings:

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

Click Create Web Service. Once deployed, access /campaign-analysis using your public Render URL.