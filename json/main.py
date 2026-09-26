from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()

# -------------------------------------------------
# Health check endpoint
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"message": "US Stocks API is running"}


#-------------------------------------------------
# API endpoint for campaign analysis
@app.get("/campaign-analysis-json", response_class=HTMLResponse)
def get_campaign_analysis():
    # Load data
    df = pd.read_csv("skin clinic campaign.csv")
    df['Response_Num'] = df['Response_to_Campaign'].apply(lambda x: 1 if x == 'Yes' else 0)

    # 1. Gender
    gender_df = df.groupby('Gender')['Response_Num'].mean().mul(100).round(2).reset_index()
    gender_df.columns = ['Gender', 'Response Rate (%)']

    # 2. Age Group (reindexed for sequential order)
    age_df = df.groupby('AgeGroup')['Response_Num'].mean().mul(100).round(2).reindex(['<30', '30-50', '>50']).reset_index()
    age_df.columns = ['Age Group', 'Response Rate (%)']

    # 3. Purchase in Last Quarter
    purchase_df = df.groupby('Purchase_Last_Quarter')['Response_Num'].mean().mul(100).round(2).reset_index()
    purchase_df.columns = ['Purchase in Last Quarter', 'Response Rate (%)']

    # 4. Product Usage
    def categorize_usage(x):
        if x <= 4: return '1-4'
        elif x <= 8: return '5-8'
        else: return '>8'
    
    df['Product_Usage'] = df['Unique_Products_Purchased'].apply(categorize_usage)
    usage_df = df.groupby('Product_Usage')['Response_Num'].mean().mul(100).round(2).reindex(['1-4', '5-8', '>8']).reset_index()
    usage_df.columns = ['Unique Products Purchased', 'Response Rate (%)']

    html_content = f"""
    <html>
        <head>
            <title>Campaign Analysis</title>
            <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #000000;
                color: #f9f9f9;
            }}
            .table-row {{
                display: flex;
                gap: 40px;
                margin-bottom: 40px;
                flex-wrap: wrap;
            }}
            .table-card {{
                flex: 1;
                min-width: 300px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #444;
                padding: 12px 8px;
                text-align: center;
            }}
            th {{
                background-color: #111;
                color: #f9f9f9;
            }}
            tr:nth-child(even) {{
                background-color: #0a0a0a;
            }}
            </style>
        </head>
        <body>
            <h2><center>Campaign Analysis - Skin Clinic Marketing Campaign - By Fernanda Machado</center></h2>
            
            <!-- Row 1: Gender & Age Group -->
            <div class="table-row">
                <div class="table-card">
                    <h2><center>Gender vs Campaign Response - test excel</center></h2>
                    {gender_df.to_html(index=False)}
                </div>
                <div class="table-card">
                    <h2><center>Age Group vs Campaign Response</center></h2>
                    {age_df.to_html(index=False)}
                </div>
            </div>

            <!-- Row 2: Purchase Last Quarter & Product Usage -->
            <div class="table-row">
                <div class="table-card">
                    <h2><center>Purchase in Last Quarter vs Campaign Response</center></h2>
                    {purchase_df.to_html(index=False)}
                </div>
                <div class="table-card">
                    <h2><center>Product Usage vs Campaign Response</center></h2>
                    {usage_df.to_html(index=False)}
                </div>
            </div>
        </body>
    </html>
    """
    return html_content


# -------------------------------------------------
# API endpoint for Excel / external JSON usage
# -------------------------------------------------
@app.get("/campaign-analysis-json")
def get_campaign_analysis_json():
    df = pd.read_csv("skin clinic campaign.csv")
    df['Response_Num'] = df['Response_to_Campaign'].apply(lambda x: 1 if x == 'Yes' else 0)

    # 1. Gender
    gender_df = df.groupby('Gender')['Response_Num'].mean().mul(100).round(2).reset_index()
    gender_df.columns = ['Gender', 'Response_Rate']

    # 2. Age Group
    age_df = df.groupby('AgeGroup')['Response_Num'].mean().mul(100).round(2).reindex(['<30', '30-50', '>50']).reset_index()
    age_df.columns = ['Age_Group', 'Response_Rate']

    # 3. Purchase Last Quarter
    purchase_df = df.groupby('Purchase_Last_Quarter')['Response_Num'].mean().mul(100).round(2).reset_index()
    purchase_df.columns = ['Purchase_Last_Quarter', 'Response_Rate']

    # 4. Product Usage
    def categorize_usage(x):
        if x <= 4: return '1-4'
        elif x <= 8: return '5-8'
        else: return '>8'
    
    df['Product_Usage'] = df['Unique_Products_Purchased'].apply(categorize_usage)
    usage_df = df.groupby('Product_Usage')['Response_Num'].mean().mul(100).round(2).reindex(['1-4', '5-8', '>8']).reset_index()
    usage_df.columns = ['Product_Usage', 'Response_Rate']

    return {
        "gender": gender_df.to_dict(orient="records"),
        "age": age_df.to_dict(orient="records"),
        "purchase": purchase_df.to_dict(orient="records"),
        "usage": usage_df.to_dict(orient="records")
    }