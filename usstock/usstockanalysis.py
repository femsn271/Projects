from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import numpy as np
import pandas as pd
import yfinance as yf

# -------------------------------------------------
# Create FastAPI app
# -------------------------------------------------
app = FastAPI()


# -------------------------------------------------
# Health check endpoint
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"message": "US Stock Market API is running"}


# -------------------------------------------------
# Stock analysis function
# -------------------------------------------------
def generate_us_stock_summary():

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)

    symbols = [
        "NVDA",
        "GOOGL",
        "AAPL",
        "MSFT",
        "AMZN",
        "META",
        "AVGO",
        "TSLA",
        "ORCL",
        "PLTR",
    ]

    stockdata = yf.download(
        tickers=symbols, start=start_date, end=end_date, progress=False
    )

    closeprice_df = stockdata["Close"].copy()
    returns_df = closeprice_df.pct_change() * 100

    summary_df = pd.DataFrame({
        "Ticker": closeprice_df.columns,
        "Max_Value": closeprice_df.max().values,
        "Min_Value": closeprice_df.min().values,
        "Current_Value": closeprice_df.iloc[-1].values,
        "Avg_Daily_Return_%": returns_df.mean().values,
        "Volatility_%": returns_df.std().values,
    })

    # Clean NaNs by replacing them with None (converts cleanly to JSON null)
    summary_df = summary_df.round(4).replace({np.nan: None})

    return summary_df


# -------------------------------------------------
# API endpoint returning JSON data
# -------------------------------------------------
@app.get("/us-stocks")
def get_us_stock_summary():
    df = generate_us_stock_summary()
    return df.to_dict(orient="records")


# -------------------------------------------------
# HTML frontend embedded directly in endpoint
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>US Stock Market Summary</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }
            button {
                padding: 10px 16px;
                font-size: 16px;
                margin-bottom: 20px;
                cursor: pointer;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f4f4f4;
            }
        </style>
    </head>
    <body>

        <h2>US Stock Market Summary</h2>

        <button onclick="loadData()">Load Summary</button>

        <table id="summaryTable">
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Max Value</th>
                    <th>Min Value</th>
                    <th>Current Value</th>
                    <th>Avg Daily Return (%)</th>
                    <th>Volatility (%)</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>

        <script>
            function loadData() {
                fetch('/us-stocks')
                    .then(response => response.json())
                    .then(data => {
                        const tbody = document.querySelector('#summaryTable tbody');
                        tbody.innerHTML = '';

                        data.forEach(row => {
                            const tr = document.createElement('tr');
                            tr.innerHTML = `
                                <td>${row.Ticker}</td>
                                <td>${row.Max_Value ?? 'N/A'}</td>
                                <td>${row.Min_Value ?? 'N/A'}</td>
                                <td>${row.Current_Value ?? 'N/A'}</td>
                                <td>${row["Avg_Daily_Return_%"] ?? 'N/A'}</td>
                                <td>${row["Volatility_%"] ?? 'N/A'}</td>
                            `;
                            tbody.appendChild(tr);
                        });
                    })
                    .catch(error => {
                        alert('Error fetching data');
                        console.error(error);
                    });
            }
        </script>

    </body>
    </html>
    """

    return html_content