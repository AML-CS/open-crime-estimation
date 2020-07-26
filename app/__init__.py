import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime as dt


#Here we load a GeoJSON file containing the geometry information for US counties, where feature.id is a FIPS code.

import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash('Visualization page', suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
  
)

app.layout = dbc.Container(fluid=False, children=[
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    ## Top

    html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("dash-logo.png"),
                        id="logo",
                        style={
                            "height": "60px",
                            "width": "auto",
                            "margin-bottom": "25px",
                        },
                    )
                ],
                className="one-third column",
                style = {'width':'10%'} 
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "Visualizador",
                                style={"margin-bottom": "0px",'textAlign': 'center'},
                            ),
                            html.H5(
                                "Proyecto", style={"margin-top": "0px",'textAlign': 'center'}
                            ),
                        ]
                    )
                ],
                className="one-half column",
                id="title",
                style = {'width':'60%'}
            ),
            html.Div(
                [
                    html.A(
                        html.Button("Más información", id="learn-more-button"),
                        href="https://github.com/rsconsuegra/visualization_page",
                    )
                ],
                className="one-third column",
                id="button",
                style = {'width':'30%'}
            ),
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px"}
    ),

    # content will be rendered in this element
    dbc.Row([
      dbc.Col(
        dbc.Card(
          [
            dbc.FormGroup([
              html.Label('Sexo'),
              dcc.RadioItems(
                options=[
                    {'label': 'Femenino', 'value': 'F'},
                    {'label': 'Masculino', 'value': 'M'},
                ],
                value='F'
              ),
              dcc.Input(
                id="age",
                type="number",
                placeholder="Edad",
              )]),
              dbc.FormGroup([
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=dt(2000, 8, 5),
                    max_date_allowed=dt(2019, 2, 1),
                    initial_visible_month=dt(2019, 1, 1),
                    start_date=dt(2018, 12, 1).date(),
                    end_date=dt(2019, 1, 7).date()
                ),
            ]),
        ]),md=4),
      dbc.Col(dcc.Graph(id="cluster-graph"), md=8)
      ],align="center",)
    ])


@app.callback(
    Output("cluster-graph", "figure"),
    [
        dash.dependencies.Input('my-date-picker-range', 'start_date'),
        dash.dependencies.Input('my-date-picker-range', 'end_date')
    ],
)
def make_graph(date_start, date_end):
  fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                             color_continuous_scale="Viridis",
                             range_color=(0, 12),
                             mapbox_style="carto-positron",
                             zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                             opacity=0.5,
                             labels={'unemp':'unemployment rate'}
                            )
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  return fig

def create_app():
  # App settings
  return app