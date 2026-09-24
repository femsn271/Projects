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
        "Company_Name": [yf.Ticker(ticker).info.get("shortName", "N/A") for ticker in closeprice_df.columns],
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
    <title>US Stock Market Summary - Tech Companies - By Fernanda Machado</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #000000;
            color: #f9f9f9;
        }
        button {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            font-size: 16px;
            margin-bottom: 20px;
            cursor: pointer;
            background-color: #222;
            color: #f9f9f9;
            border: 1px solid #444;
            border-radius: 4px;
        }
        button:hover:not(:disabled) {
            background-color: #333;
        }
        button:disabled {
            cursor: not-allowed;
            opacity: 0.7;
        }
        /* CSS Spinner Styling */
        .spinner {
            width: 16px;
            height: 16px;
            border: 2px solid #f9f9f9;
            border-bottom-color: transparent;
            border-radius: 50%;
            display: inline-block;
            box-sizing: border-box;
            animation: rotation 1s linear infinite;
        }
        @keyframes rotation {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #444;
            padding: 12px 8px;
            text-align: center;
        }
        th {
            background-color: #111;
            color: #f9f9f9;
        }
        tr:nth-child(even) {
            background-color: #0a0a0a;
        }
        /* Dynamic return colors */
        .positive {
            color: #4caf50; /* Clean, visible green on dark background */
            font-weight: bold;
        }
        .negative {
            color: #f44336; /* Bright, clear red */
            font-weight: bold;
        }
    </style>
</head>
<body>

    <h2>US Stock Market Summary - Tech Companies - By Fernanda Machado</h2>

    <button id="loadBtn" onclick="loadData()">
        <span id="btnText">Load Summary</span>
    </button>

    <table id="summaryTable">
        <thead>
            <tr>
                <th>Ticker</th>
                <th>Company Name</th>
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
            const btn = document.getElementById('loadBtn');
            const btnText = document.getElementById('btnText');
            
            // 1. Start loading state
            btn.disabled = true;
            btnText.textContent = 'Loading...';
            
            // Add the spinner element dynamically
            const spinner = document.createElement('span');
            spinner.className = 'spinner';
            spinner.id = 'btnSpinner';
            btn.prepend(spinner);

            fetch('/us-stocks')
                .then(response => response.json())
                .then(data => {
                    const tbody = document.querySelector('#summaryTable tbody');
                    tbody.innerHTML = '';

                    data.forEach(row => {
                        const tr = document.createElement('tr');
                        
                        // Parse return value to decide text color class
                        const returnValue = parseFloat(row["Avg_Daily_Return_%"]);
                        let returnClass = '';
                        
                        if (!isNaN(returnValue)) {
                            if (returnValue > 0) returnClass = 'class="positive"';
                            else if (returnValue < 0) returnClass = 'class="negative"';
                        }

                        tr.innerHTML = `
                            <td>${row.Ticker}</td>
                            <td>${row.Company_Name ?? 'N/A'}</td>
                            <td>${row.Max_Value ?? 'N/A'}</td>
                            <td>${row.Min_Value ?? 'N/A'}</td>
                            <td>${row.Current_Value ?? 'N/A'}</td>
                            <td ${returnClass}>${row["Avg_Daily_Return_%"] ?? 'N/A'}</td>
                            <td>${row["Volatility_%"] ?? 'N/A'}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                })
                .catch(error => {
                    alert('Error fetching data');
                    console.error(error);
                })
                .finally(() => {
                    // 2. Reset loading state when fetch completes (success or failure)
                    btn.disabled = false;
                    btnText.textContent = 'Load Summary';
                    const activeSpinner = document.getElementById('btnSpinner');
                    if (activeSpinner) activeSpinner.remove();
                });
        }
    </script>

</body>
</html>

    """

    return html_content