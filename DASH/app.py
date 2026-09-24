# Dash App: Train on Server CSV -> Upload Test CSV -> Logistic Regression -> Probabilities -> Threshold Counts
# ----------------------------------------------------------------------------------
# Steps:
# 1. Model is trained once using local TRAIN CSV when app starts
# 2. User uploads only TEST CSV
# 3. No feature scaling (pure BLR)
# 4. Threshold dropdown controls defaulter / non-defaulter counts

# Run: python app.py  |  Then open http://127.0.0.1:8050

import base64
import io
import pandas as pd
import numpy as np

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from sklearn.linear_model import LogisticRegression

# ===============================
# ====== TRAIN MODEL ONCE =======
# ===============================


train_df = pd.read_csv('BANK LOAN.csv')

if 'DEFAULTER' not in train_df.columns:
    raise ValueError("Training file must contain 'DEFAULTER' column")

X_train = train_df.drop(columns=['DEFAULTER'])
y_train = train_df['DEFAULTER']

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

FEATURE_COLUMNS = X_train.columns.tolist()

print("Model trained successfully on server startup")


# ===============================
# ===== DASH APP SETUP ==========
# ===============================

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Credit Default Prediction App"


# ===============================
# ========= LAYOUT ==============
# ===============================

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H2("💳 Credit Default Prediction",
                         className="text-center text-primary mb-4"), width=12)
    ]),

    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Upload TEST CSV File"),
                dbc.CardBody([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag & Drop or ', html.A('Select CSV File')
                        ]),
                        style={
                            'width': '100%',
                            'height': '80px',
                            'lineHeight': '80px',
                            'borderWidth': '2px',
                            'borderStyle': 'dashed',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'backgroundColor': '#f8f9fa'
                        },
                        multiple=False
                    ),
                    html.Div(id='file-name', className="mt-2 text-success")
                ])
            ], className="shadow")
        ], md=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Select Probability Threshold"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='threshold-dropdown',
                        options=[{'label': f'{i/10:.1f}', 'value': i/10} for i in range(1, 10)],
                        value=0.5,
                        clearable=False
                    ),
                    html.Div(id='count-output', className="mt-3 fs-5")
                ])
            ], className="shadow")
        ], md=6)

    ], className="mb-4"),


    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Probability Distribution"),
                dbc.CardBody([
                    dcc.Graph(id='prob-plot')
                ])
            ], className="shadow")
        ], md=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Prediction Preview (Top 10 Rows)"),
                dbc.CardBody([
                    html.Div(id='table-preview')
                ])
            ], className="shadow")
        ], md=6)

    ])

], fluid=True, className="p-4")


# ===============================
# ===== HELPER FUNCTION =========
# ===============================

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))


# ===============================
# ========= CALLBACKS ===========
# ===============================

@app.callback(
    Output('file-name', 'children'),
    Input('upload-data', 'filename')
)
def show_filename(filename):
    if filename:
        return f"Uploaded: {filename}"
    return ""


@app.callback(
    Output('prob-plot', 'figure'),
    Output('table-preview', 'children'),
    Output('count-output', 'children'),
    Input('upload-data', 'contents'),
    Input('threshold-dropdown', 'value'),
    prevent_initial_call=True
)
def predict_test_data(contents, threshold):

    # -------- Load TEST data --------
    test_df = parse_contents(contents)

    # -------- Validate columns --------
    missing_cols = set(FEATURE_COLUMNS) - set(test_df.columns)
    if missing_cols:
        return {}, f"Missing columns in test file: {missing_cols}", ""

    X_test = test_df[FEATURE_COLUMNS]

    # -------- Predict probabilities --------
    probs = model.predict_proba(X_test)[:, 1]

    test_df['Default_Prob'] = probs
    test_df['Pred_Label'] = (test_df['Default_Prob'] >= threshold).astype(int)

    # -------- Counts --------
    defaulters = int((test_df['Pred_Label'] == 1).sum())
    non_defaulters = int((test_df['Pred_Label'] == 0).sum())

    count_text = html.Div([
        html.P(f"Threshold Selected: {threshold}"),
        html.P(f"Predicted Defaulters: {defaulters}", className="text-danger fw-bold"),
        html.P(f"Predicted Non-Defaulters: {non_defaulters}", className="text-success fw-bold")
    ])

    # -------- Probability Distribution Plot --------
    fig = px.histogram(
        test_df,
        x='Default_Prob',
        nbins=20,
        title='Distribution of Predicted Default Probabilities'
    )
    fig.add_vline(x=threshold, line_dash="dash")
    fig.update_layout(template='plotly_white')

    # -------- Table Preview --------
    filtered_df = test_df[test_df['Default_Prob'] >= threshold]

    if filtered_df.empty:
        preview_table = html.P(
            "No records found above selected threshold.",
            className="text-warning fw-bold"
        )
    else:
        preview_df = filtered_df[['Default_Prob', 'Pred_Label']].round(3).head(10)

        preview_table = dbc.Table.from_dataframe(
            preview_df,
            striped=True, bordered=True, hover=True, size='sm'
        )

    return fig, preview_table, count_text


# ===============================
# ========= RUN APP =============
# ===============================

if __name__ == '__main__':
    #app.run_server(debug=True)
    import webbrowser
    from threading import Timer

    url = "http://127.0.0.1:8050"
    Timer(1, lambda: webbrowser.open(url)).start()

    app.run(debug=True)