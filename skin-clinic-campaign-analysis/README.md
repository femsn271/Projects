# Skin Clinic Marketing Campaign Analysis

## Live Applications

### HTML Campaign Analysis

https://campaign-analysis-5e6d.onrender.com/campaign-analysis

Web-based presentation of the campaign response-rate analysis.

### JSON API

https://campaign-analysis-json.onrender.com/campaign-analysis-json

Machine-readable JSON endpoint used to provide the campaign analysis to external applications, including the Excel workflow.

---

## Project Overview

This project analyzes customer responses to a targeted skin clinic marketing campaign.

The solution combines **Python, Pandas, FastAPI, JSON and Microsoft Excel** to transform campaign data into response-rate analysis that can be viewed through a web interface and consumed by an Excel workbook.

The analysis focuses on identifying differences in campaign response rates across customer demographics and purchasing behaviour.

The project was originally developed as part of a FastAPI model-deployment module and has been adapted here as a portfolio project to demonstrate practical data analysis, API development and application integration.

---

## Business Objective

The objective is to analyse campaign response patterns across different customer segments and provide information that can support future marketing targeting and campaign planning.

The application examines four main dimensions:

- Gender
- Age group
- Purchase activity in the last quarter
- Number of unique products purchased

The resulting response rates can be accessed through the web application, JSON API and Excel workflow.

---

## Data Analysis

The campaign response is converted into a numerical variable:

Yes → 1
Other response → 0

Response rates are then calculated as percentages for each customer segment.

### Gender

Campaign response rates are calculated separately for:

- Female
- Male

### Age Group

Customers are grouped into:

- `<30`
- `30–50`
- `>50`

### Purchase in Last Quarter

Customers are segmented according to whether they purchased during the last quarter:

- Yes
- No

### Product Usage

Customers are grouped according to the number of unique products purchased:

| Product Group | Definition |
|---|---|
| 1–4 | Up to 4 products |
| 5–8 | 5 to 8 products |
| >8 | More than 8 products |

These groupings are implemented directly in the application logic.

---

## Application Architecture

The project provides two FastAPI-based interfaces.
                    Campaign CSV Dataset
                            │
                            ▼
                       Pandas
                            │
                  Campaign Analysis
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
       HTML FastAPI App             JSON FastAPI App
              │                           │
              ▼                           ▼
       Web Analysis Page             JSON Response
                                          │
                                          ▼
                                   Excel Workbook
                                  Skin campaign.xlsm


Response rates are then calculated for each customer segment.
Gender
Response rates are calculated for:
- Female
- Male
Age Group
Customers are grouped into:
- <30
- 30-50
- >50
Purchase in Last Quarter
Customers are segmented according to recent purchasing activity:
- Yes
- No
Unique Products Purchased
Product usage is grouped into:
Group	Definition
1-4	Up to 4 unique products
5-8	5 to 8 unique products
>8	More than 8 unique products


## Solution Architecture
The project contains two FastAPI applications serving different purposes.
                    Campaign CSV Dataset
                            │
                            ▼
                       Pandas
                            │
                  Campaign Analysis
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
       HTML FastAPI App             JSON FastAPI App
              │                           │
              ▼                           ▼
       Web Analysis Page             JSON Response
                                          │
                                          ▼
                                   Excel Workbook
                                  Skin campaign.xlsm

### HTML Analysis
The HTML application processes the campaign dataset and generates a web page containing response-rate tables.

### JSON API
The JSON application performs the same campaign analysis and returns structured JSON data.

The JSON endpoint is designed for consumption by external applications and is used as part of the Excel integration workflow.

### Excel Integration

The project includes:

Skin campaign.xlsm

The Excel workbook uses the campaign analysis data provided through the JSON/API workflow and presents the resulting metrics in an Excel-based format.

This demonstrates how a Python API can provide analytical data to a business-oriented tool such as Microsoft Excel.

## API Endpoints

### HTML Application

Health Check

GET /health

Returns:
{
  "message": "API is running"
}

Campaign Analysis

GET /campaign-analysis

Returns an HTML page containing campaign response-rate tables for:
- Gender
- Age group
- Purchase in the last quarter
- Product usage
Response type:
text/html

### JSON Application
Health Check
GET /health

Returns:
{
  "message": "API is running"
}

Campaign Analysis JSON
GET /campaign-analysis-json

Returns structured JSON containing four analytical sections:
{
  "gender": [],
  "age": [],
  "purchase": [],
  "usage": []
}

The JSON response can be consumed by external applications, including the Excel workflow used in this project.
Example JSON Structure
The API returns the analysis in four sections:
{
  "gender": [
    {
      "Gender": "Female",
      "Response_Rate": 0.0
    }
  ],
  "age": [
    {
      "Age_Group": "<30",
      "Response_Rate": 0.0
    }
  ],
  "purchase": [
    {
      "Purchase_Last_Quarter": "Yes",
      "Response_Rate": 0.0
    }
  ],
  "usage": [
    {
      "Product_Usage": "1-4",
      "Response_Rate": 0.0
    }
  ]
}

The actual values are generated dynamically from the campaign dataset.

### Excel Integration

The project includes an Excel macro-enabled workbook:

Skin campaign.xlsm

The Excel component provides a business-friendly way to work with the campaign analysis produced by the API.

The integration demonstrates the following workflow:
Python / Pandas
       │
       ▼
FastAPI JSON Endpoint
       │
       ▼
JSON Data
       │
       ▼
Excel Workbook
       │
       ▼
Campaign Analysis

This provides an example of integrating a Python-based analytical API with an existing business productivity tool.

## Technology Stack
Technology	Purpose
Python	Application development
Pandas	Data processing and analysis
FastAPI	REST API development
Uvicorn	ASGI application server
JSON	Data exchange format
HTML	Web presentation
CSS	Web interface styling
Microsoft Excel	Business analysis and API integration
VBA	Excel automation/integration
Render	Cloud deployment


## Project Structure
skin-clinic-campaign-analysis/
│
├── app.py
├── campaign_json.py
├── skin_clinic_campaign.csv
├── Skin campaign.xlsm
├── requirements.txt
└── README.md

app.py

Main FastAPI application for the HTML campaign analysis.

Responsibilities include:
- Loading the campaign dataset
- Calculating response rates
- Generating the HTML analysis page
- Providing the health-check endpoint

campaign_json.py

FastAPI application providing the machine-readable campaign analysis endpoint.

Responsibilities include:
- Loading the campaign dataset
- Calculating the same campaign metrics
- Returning structured JSON
- Providing a health-check endpoint

skin_clinic_campaign.csv

Source campaign dataset used by the Python applications.
Skin campaign.xlsm

Excel workbook used as part of the JSON/API integration workflow.

requirements.txt

Python dependencies required to run the applications.

## Local Setup
1. Create a virtual environment
python -m venv .venv

2. Activate the environment
Windows:
.venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

The project requires:
fastapi
uvicorn
pandas

Running the HTML Application
From the project directory:
uvicorn app:app --reload

The application will run locally at:
http://127.0.0.1:8000

Open:
http://127.0.0.1:8000/campaign-analysis

Running the JSON Application
The JSON application is a separate FastAPI application.
Run:
uvicorn campaign_json:app --reload --port 8001

Then open:
http://127.0.0.1:8001/campaign-analysis-json

## Deployment
The two applications are deployed as separate Render services.
HTML Application
Start command:
uvicorn app:app --host 0.0.0.0 --port $PORT

JSON Application
Start command:
uvicorn campaign_json:app --host 0.0.0.0 --port $PORT

The applications load the CSV dataset from their application directory when the analysis endpoint is requested.
Data Processing Workflow
The analytical workflow is:
Campaign CSV
     │
     ▼
Load with Pandas
     │
     ▼
Convert campaign response to numeric value
     │
     ▼
Create customer segments
     │
     ▼
Calculate response rates
     │
     ├──────────────────────┐
     ▼                      ▼
HTML Output             JSON Output
                             │
                             ▼
                       Excel Workflow

Response rates are calculated using grouped customer segments and the mean of the binary response variable, converted to percentages.

## Key Learning Outcomes
This project demonstrates practical experience with:
- CSV data processing using Pandas
- Exploratory customer segmentation
- Grouped response-rate analysis
- Business-oriented data analysis
- REST API development with FastAPI
- HTML responses from an API
- Structured JSON API responses
- API-to-Excel integration
- Microsoft Excel/VBA integration
- Running applications with Uvicorn
- Deploying Python APIs to Render

## Limitations
This project is a descriptive analytics application, not a predictive machine-learning model.
The response rates describe observed differences between customer segments but do not establish causal relationships.
The current implementation does not include:
- Predictive modelling
- Statistical significance testing
- A/B testing
- Causal inference
- Automated campaign optimisation
- Real-time customer data
- Database-backed storage
- Authentication for the API

## Future Improvements
Potential improvements include:
- Add interactive visualisations
- Add statistical significance testing
- Add predictive modelling for campaign response
- Add additional customer segmentation variables
- Add database integration
- Add automated campaign reporting
- Add API authentication
- Add automated API tests
- Add CI/CD deployment
- Add automated Excel refresh workflows

## Disclaimer
This project is an educational and portfolio demonstration of customer campaign analysis, API development and application integration.
The results are descriptive insights derived from the provided campaign dataset and should not be interpreted as evidence of causal relationships.