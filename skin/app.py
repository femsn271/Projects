from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()

@app.get("/campaign-analysis", response_class=HTMLResponse)
def get_campaign_analysis():
    # Load data
    df = pd.read_csv("skin clinic campaign.csv")
    df['Response_Num'] = df['Response_to_Campaign'].apply(lambda x: 1 if x == 'Yes' else 0)

    # 1. Gender
    gender_df = df.groupby('Gender')['Response_Num'].mean().mul(100).round(2).reset_index()
    gender_df.columns = ['Gender', 'Response Rate (%)']

    # 2. Age Group
    age_df = df.groupby('AgeGroup')['Response_Num'].mean().mul(100).round(2).reset_index()
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
            /* Flexbox wrapper to align two cards side-by-side */
            .table-row {{
                display: flex;
                gap: 40px;
                margin-bottom: 40px;
                flex-wrap: wrap; /* Wraps onto a new line on smaller screens */
            }}
            .table-card {{
                flex: 1; /* Makes both cards take equal width */
                min-width: 300px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%; /* Table expands to fill its card width */
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
        <h2> <center> Campaign Analysis - Skin Clinic Marketing Campaign - By Fernanda Machado</h2>
            <!-- Row 1: Gender & Age Group -->
            <div class="table-row">
                <div class="table-card">
                    <h2> <center>Gender vs Campaign Response - test excel</h2>
                    {gender_df.to_html(index=False)}
                </div>
                <div class="table-card">
                    <h2> <center>Age Group vs Campaign Response</h2>
                    {age_df.to_html(index=False)}
                </div>
            </div>

            <!-- Row 2: Purchase Last Quarter & Product Usage -->
            <div class="table-row">
                <div class="table-card">
                    <h2> <center>Purchase in Last Quarter vs Campaign Response</h2>
                    {purchase_df.to_html(index=False)}
                </div>
                <div class="table-card">
                    <h2> <center>Product Usage vs Campaign Response</h2>
                    {usage_df.to_html(index=False)}
                </div>
            </div>
        </body>
    </html>
    """
    return html_content