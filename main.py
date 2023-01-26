import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pickle
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = html.Div(
    className="container",
    children=[
        html.Div(
            [
            html.Title('Credit Risk Probability Prediction'),
                html.H1('Credit Risk Classification'),
            html.Header('Use this app to predict risk probability based on borrower information')
            ]
        ),
        dbc.Row([
            dbc.Col([
                dbc.Form([
                    html.Label("The total principal of the loan", className="text-primary"),
                    dbc.Input(id="loan-amnt", placeholder="in $ min-1000, max-40000", min=1000, max=40000, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("The term length of the loan", className="text-primary"),
                    dcc.Dropdown(
                        id="term",
                        options=[
                            {"label": "36 Months", "value": 36},
                            {"label": "60 Months", "value": 60},
                        ],
                        value="Select",
                        className="form-control"
                    ),
                ]),
                dbc.Form([
                    html.Label("Interest Rate", className="text-primary"),
                    dbc.Input(id="int-rate", placeholder="in % min-5, max-30", min=5, max=30, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Grade (The quality of the loan)", className="text-primary"),
                    dcc.Dropdown(
                        id="grade",
                        options=[
                            {"label": "A", "value": 'A'},
                            {"label": "B", "value": 'B'},
                            {"label": "C", "value": 'C'},
                            {"label": "D", "value": 'D'},
                            {"label": "E", "value": 'E'},
                            {"label": "F", "value": 'F'},
                            {"label": "G", "value": 'G'},
                            {"label": "H", "value": 'H'},
                        ],
                        value="Select",
                        className="form-control"
                    ),
                ]),
                dbc.Form([
                    html.Label("Borrower’s home status", className="text-primary"),
                    dcc.Dropdown(
                        id="home-ownership",
                        options=[
                            {"label": "Rent", "value": 'RENT'},
                            {"label": "Mortgage", "value": 'MORTGAGE'},
                            {"label": "Own", "value": 'OWN'},
                        ],
                        value="Select",
                        className="form-control"
                    ),
                ]),
                dbc.Form([
                    html.Label("Borrower’s reported annual income", className="text-primary"),
                    dbc.Input(id="annual-inc", placeholder="in $ min-4500, max-9000000", min=4500, max=9000000, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Verification Status", className="text-primary"),
                    dcc.Dropdown(
                        id="verification-status",
                        options=[
                            {"label": "Verified", "value": 'Verified'},
                            {"label": "Not Verified", "value": 'Not Verified'},
                            {"label": "Source Verified", "value": 'Source Verified'},
                        ],
                        value="Select",
                        className="form-control"
                    ),
                ]),
                dbc.Form([
                    html.Label("Title", className="text-primary"),
                    dcc.Dropdown(
                        id="title",
                        options=[
                            {"label": "Debt consolidation", "value": 'Debt consolidation'},
                            {"label": "Credit card refinancing", "value": 'Credit card refinancing'},
                            {"label": "Home improvement", "value": 'Source Verified'},
                            {"label": "Other", "value": 'Other'}
                        ],
                        value="Select",
                        className="form-control"
                    ),
                ]),
            ]),
            dbc.Col([
                dbc.Form([
                    html.Label("Debt To Income Ratio", className="text-primary"),
                    dbc.Input(id="dti", placeholder="Monthly Debt Payments/reported Monthly Income min-0, max-60", min=0, max=60, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Number of open credit lines on the borrower’s credit file.", className="text-primary"),
                    dbc.Input(id="open-acc", placeholder="min-1, max-30", min=1, max=30, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Total credit revolving balance.", className="text-primary"),
                    dbc.Input(id="revol-bal", placeholder="min-0, max-100000", min=0, max=100000, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Revolving Line Utilization Rate", className="text-primary"),
                    dbc.Input(id="revol-util", placeholder="min-0, max-150", min=0, max=150, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("The total number of credit lines currently in the borrower's credit file", className="text-primary"),
                    dbc.Input(id="total-acc", placeholder="min-4, max-70", min=4, max=70, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Initial List Status", className="text-primary"),
                    dcc.Dropdown(
                        id="initial-list-status",
                        options=[
                            {"label": "Fractional", "value": 'f'},
                            {"label": "Whole", "value": 'w'},
                        ],
                        value="Select",
                        className="form-control"
                    ),
                ]),
                dbc.Form([
                    html.Label("Payments received to date for total amount funded", className="text-primary"),
                    dbc.Input(id="total-pymnt", placeholder="in $ min-0, max-45000", min=0, max=45000, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Interest received to date", className="text-primary"),
                    dbc.Input(id="total-rec-int", placeholder="in $ min-0, max-4000", min=0, max=4000, type="number", className="form-control"),
                ]),
                dbc.Form([
                    html.Label("Total current balance of all accounts", className="text-primary"),
                    dbc.Input(id="tot-cur-bal", placeholder="in $ min-0, max-700000", min=0, max=700000, type="number", className="form-control"),
                ]),
            ])
                ]),
            dbc.Button("Predict Probability of Risk", id='submit-button', className="btn btn-info",
                       n_clicks=0, style={'text-align': 'center', 'margin': 'auto', 'display':'flex', 'padding': '10px'}),
            html.Div(id='outputs', className='alert alert-dismissible alert-warning', style={'text-align': 'center'})
    ]
)

@app.callback(
    Output('outputs', 'children'),
    Input('submit-button', 'n_clicks'),
    State('loan-amnt', 'value'),
    State('term', 'value'),
    State('int-rate', 'value'),
    State('grade', 'value'),
    State('home-ownership', 'value'),
    State('annual-inc', 'value'),
    State('verification-status', 'value'),
    State('title', 'value'),
    State('dti', 'value'),
    State('open-acc', 'value'),
    State('revol-bal', 'value'),
    State('revol-util', 'value'),
    State('total-acc', 'value'),
    State('initial-list-status', 'value'),
    State('total-pymnt', 'value'),
    State('total-rec-int', 'value'),
    State('tot-cur-bal', 'value')
)
def predict(n_clicks, loan_amnt, term, int_rate, grade, home_ownership, annual_inc, verification_status, title, dti,
            open_acc, revol_bal, revol_util, total_acc, initial_list_status, total_pymnt, total_rec_int, tot_cur_bal):

    if n_clicks == 0:
        return ''

    df_dict = {
        'loan_amnt': loan_amnt,
        'term': term,
        'int_rate': int_rate,
        'grade': grade,
        'home_ownership': home_ownership,
        'annual_inc': annual_inc,
        'verification_status': verification_status,
        'title': title,
        'dti': dti,
        'open_acc': open_acc,
        'revol_bal': revol_bal,
        'revol_util': revol_util,
        'total_acc': total_acc,
        'initial_list_status': initial_list_status,
        'total_pymnt': total_pymnt,
        'total_rec_int': total_rec_int,
        'tot_cur_bal': tot_cur_bal
    }

    with open('credit-risk.pkl', 'rb') as f:
        mod = pickle.load(f)

    inp = pd.DataFrame(df_dict, index=[0])
    try:
        proba = round(mod.predict_proba(inp)[0][1] * 100, 2)
    except Exception as e:
        print(str(e))
        return html.P('Please input all the values in the form to get the output.')

    return html.P(f'Probability of risk is {proba}',className='mb-0')

if __name__ == '__main__':
    app.run_server()
