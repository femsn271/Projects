# US Stock Market Analysis

A Python and FastAPI application that retrieves historical market data for ten major US-listed technology companies, calculates descriptive stock statistics, and presents the results through both a JSON API and a browser-based dashboard.

**Live application:** https://us-stock-6y96.onrender.com

> This project performs descriptive financial data analysis. It does not forecast stock prices or provide investment recommendations.

## Project overview

The application retrieves approximately one calendar year of historical prices using `yfinance`. It downloads the selected tickers in a single batch, calculates summary statistics with Pandas and NumPy, and displays the results in an HTML table with positive and negative daily returns highlighted.

### Companies covered

| Ticker | Company |
| --- | --- |
| NVDA | NVIDIA |
| GOOGL | Alphabet |
| AAPL | Apple |
| MSFT | Microsoft |
| AMZN | Amazon |
| META | Meta Platforms |
| AVGO | Broadcom |
| TSLA | Tesla |
| ORCL | Oracle |
| PLTR | Palantir Technologies |

## Analysis and methodology

For each ticker, the application calculates:

- **Maximum closing price:** highest closing price in the downloaded period.
- **Minimum closing price:** lowest closing price in the downloaded period.
- **Latest available closing price:** the closing price in the last downloaded observation; this is not a real-time market quote.
- **Average daily return (%):** arithmetic mean of daily percentage changes in closing prices.
- **Daily volatility (%):** sample standard deviation of daily percentage returns over the downloaded period.

Daily return is calculated as:

`daily_return_pct = (close_today / close_previous - 1) * 100`

Volatility is calculated from the standard deviation of those daily returns. It is **not annualized**. The application uses the `Close` data returned by the installed version of `yfinance`; the existing code does not explicitly set `auto_adjust`, so the price adjustment behavior can depend on the library version.

The date range starts 365 calendar days before execution and uses the execution date as the exclusive download end date. Actual observations depend on trading days and data-provider availability.

## Architecture

```text
Browser dashboard ──fetch──> FastAPI /us-stocks
                               |
                               v
                         yfinance batch download
                               |
                               v
                         Pandas / NumPy analysis
                               |
                               v
                         JSON response ──> HTML table
```

## API endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | Browser-based dashboard with a Load Summary button |
| `/health` | GET | Basic application health response |
| `/us-stocks` | GET | JSON array containing stock summary statistics |
| `/docs` | GET | FastAPI's automatically generated interactive API documentation |

The `/us-stocks` response contains the following fields for each stock:

```json
{
  "Ticker": "AAPL",
  "Company_Name": "Apple Inc.",
  "Max_Value": 0.0,
  "Min_Value": 0.0,
  "Current_Value": 0.0,
  "Avg_Daily_Return_%": 0.0,
  "Volatility_%": 0.0
}
```

**Schema illustration only:** the zeros above are placeholders, not observed prices or measured results. Numeric values change as the historical window moves. Missing statistics may be returned as `null`.

## Technology stack

- **Python** — application and analysis logic
- **FastAPI** — HTTP API and HTML delivery
- **yfinance** — historical market data retrieval
- **Pandas and NumPy** — time-series calculations and summary statistics
- **HTML, CSS and JavaScript** — browser interface and API requests
- **Uvicorn** — ASGI application server
- **Render** — application deployment

## Project structure


us-stock-analysis/
├── usstockanalysis.py
├── requirements.txt
└── README.md


## Running locally

From the project directory, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the application:

```powershell
uvicorn usstockanalysis:app --reload
```

Open `http://127.0.0.1:8000/` for the dashboard, `http://127.0.0.1:8000/docs` for interactive API documentation, or `http://127.0.0.1:8000/us-stocks` for JSON results. An internet connection is required to download market data.

## Deployment

The application is hosted on Render. For a service whose root directory is this project folder, a typical configuration is:

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
uvicorn usstockanalysis:app --host 0.0.0.0 --port $PORT
```

If the Render root directory points to the repository root instead, adjust the build/start commands or the service's root-directory setting to match the deployed file structure. Free or sleeping instances may take additional time to respond to the first request.

## Limitations

- Data comes from a third-party provider and may be delayed, unavailable, revised or incomplete.
- The latest downloaded closing price is not a live trading quote.
- The current implementation does not explicitly validate empty downloads or partially missing ticker histories before calculating all statistics.
- The `Close` price adjustment setting is not explicitly pinned in the current code.
- Every `/us-stocks` request downloads the data again, which can increase response times and encounter provider rate limits.
- The dashboard currently handles network failures generically and does not separately display detailed API errors.
- Volatility is daily and historical, not an annualized risk forecast.
- The project intentionally does not implement stock-price prediction, portfolio optimization or trading signals.

## Potential improvements

1. Explicitly configure the price-adjustment setting and document it.
2. Validate missing or empty provider responses and return appropriate HTTP errors.
3. Cache downloaded data for a limited period to reduce repeated external requests.
4. Add automated tests for the calculations and API responses using mocked market data.
5. Add request logging and user-friendly error messages in the dashboard.
6. Remove unused dependencies after checking the deployment environment.

## Learning outcomes

This project demonstrates practical experience with external data retrieval, financial time-series transformations, descriptive statistics, REST API design, browser-to-API integration and cloud deployment.

## Disclaimer

This application is an educational portfolio project. Its information is provided for demonstration purposes only and is not financial advice. Always verify market data independently before making investment decisions.
