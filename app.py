from dash import Dash,dcc,html, Output, Input, callback
from datetime import date, datetime as dt
from matplotlib import markers
import pandas as pd
import yfinance as yf
import plotly.express as px
import model as mdl

app = Dash(__name__)

server = app.server

app.layout = html.Div([html.Div(
          [
            html.P("Welcome to the Stock Dash App!", className="start",
                   style = {
                       'font-family' : 'Roboto',
                       'padding' : '30px',
                       'font-size' : '35px'
                   }),
            html.P("Input Stoke Code : ", style = {'font-size' : '20px', 'text-align' : 'left', 'padding-left' : '80px'}),
            html.Div([
              dcc.Input(id = 'company', type = "text", style = {'padding' : '6px','width' : '350px', 'background-color' : 'rgb(195, 182, 196)'}),
              html.Button('Submit', id='submit-val', n_clicks=0, style = {'padding' : '6px', 'width' : '90px', 'background-color' : 'rgb(163, 107, 164)'})
            ],style = {
                'padding' : '30px'
            }),
            html.Div([
              dcc.DatePickerRange(
              id='my-date-picker-range',
              min_date_allowed=date(1995, 8, 5),
              max_date_allowed=date(2017, 9, 19),
              initial_visible_month=date(2017, 8, 5),
              end_date=date(2017, 8, 25)
            ),
            ], style = {'padding' : '90px', 'margin-left' : '30px'}),
            html.Div([
              html.Div([
                  html.Button('Stoke Price', id='Stoke-Price', n_clicks=0, style = {'padding' : '15px', 'margin' : '10px', 'width' : '260px','font-size' : '20px', 'background-color' : 'rgb(163, 107, 164)'}),
                  html.Button('Indicators', id='Indicators', n_clicks=0, style = {'padding' : '15px','margin' : '10px', 'width' : '260px','font-size' : '20px','background-color' : 'rgb(163, 107, 164)'})
              ],
              style = {
                  'display' : 'flex',
                  'justify-content' : 'flex-start',
                  'margin' : '20px'
              }),
              html.Div([
              dcc.Input(id = 'Number_of_Days', placeholder='Number of Days', type = "number", style = {'padding' : '20px','background-color' : 'rgb(195, 182, 196)', 'margin' : '10px', 'width' : '350px'}),
              html.Button('Forcast', id='forcast', n_clicks=0, style = {'padding' : '15px', 'width' : '150px', 'font-size' : '20px', 'background-color' : 'rgb(163, 107, 164)'})
              ],style = {
                'padding' : '10px'
              }),
            ]),
          ],
        className="nav",
        style = {
       'text-align' : 'center',
       'background-color': 'rgb(239, 199, 240)'
}),
html.Div(
          [
            html.Div( [
            ],id="description", style= { 'margin' : '5px'}),
            html.Div([
            ], id="graph-content"),
            html.Div([
            ], id="main-content"),
            html.Div([
            ], id="forecast-content")
          ],
        className="content")
],
style = {
    'display' : 'flex',
    'justify-content' : 'flex-start'
})

@app.callback(
    Output('description', 'children'),
    Input('company', 'value'),
    Input('submit-val','n_clicks')
)
def company_desciption(code,n_clicks) :
    company_code = str(code)
    if n_clicks and company_code : 
        ticker = yf.Ticker(company_code)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf, orient = "index").T
        return [
            html.P(df['longName'], style= { 'font-size' : '30px'}),
            html.P(df['longBusinessSummary'])
        ]
    else : 
        return []
    
@app.callback(
    Output('graph-content', 'children'),
    Input('company', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('Stoke-Price','n_clicks')   
)

def company_stock(code, start_date, end_date, n_clicks):
    company_code = str(code)
    if code and n_clicks and range : 
      df = yf.download(company_code, start = start_date, end = end_date)
      df.reset_index(inplace = True)
      fig = get_stock_price_fig(df)
      fig.update_traces(mode= 'lines+markers')
      return dcc.Graph(figure = fig)
    else:
      []

def get_stock_price_fig(df) : 
    fig = px.line(df,
                 x='Date', y=['Open', 'Close'], title="Closing and Opening Price vs Date")
    return fig

@app.callback(
    Output('main-content', 'children'),
    Input('company', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('Indicators', 'n_clicks'),
)

def get_EWA_val(code, start_date, end_date, n_clicks) : 
    company_code = str(code)
    if company_code and n_clicks :
      df = yf.download(company_code, start = start_date, end = end_date) 
      df.reset_index(inplace = True)
      df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
      fig = px.line(df, x = 'Date', y = 'EWA_20', title="Exponential Moving Average vs Date")
      fig.update_traces(mode= 'lines+markers')
      return dcc.Graph(figure=fig)
    else : 
       return []

@app.callback(
   Output('forecast-content', 'children'),
   Input('company', 'value'),
   Input('Number_of_Days', 'value'),
   Input('forcast', 'n_clicks')
)

def get_forcast(code, number_of_days, n_clicks):
    company_code = str(code)
    if company_code and number_of_days and n_clicks:
      predict = mdl.get_prediction(code, number_of_days)
      fig = px.line(predict, x = 'Days', y = 'Stock Price', title="Prediction Close Price vs days")
      fig.update_traces(mode = 'lines+markers')
      return dcc.Graph(figure=fig)
    else : 
      return []

if __name__ == '__main__':
    app.run_server(debug=True)

