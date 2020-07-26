import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('Visualization page', external_stylesheets=external_stylesheets)

app.layout = html.Div([
  html.Label('Sexo'),
  dcc.RadioItems(
    options=[
        {'label': 'Femenino', 'value': 'F'},
        {'label': 'Masculino', 'value': 'M'},
    ],
    value='F'
  ),
  html.Label('Edad'),
  dcc.Input(
    id="age",
    type="number",
    placeholder="Edad",
  ),
], style={'width': '500'})

def create_app():
  # App settings
  return app