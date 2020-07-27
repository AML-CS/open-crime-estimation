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
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
app.title='Visualizador'


app.layout = dbc.Container(fluid=False, children=[
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    ## Top

    html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("AML.png"),
                        id="logo",
                        style={
                            "height": "120px",
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
                        html.Button("Más información", id="learn-more-button"
                            ,style ={"font-family": '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif',"background-color":"transparent","border":"1px transparent #bbb",'color':'#ffffff'}),
                        href="https://github.com/rsconsuegra/visualization_page",
                    ),
                ],
                className="one-third column",
                id="button",
                style = {'width':'30%',"justify":"center", "align":"center","margin-top":"20px"}
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
                min=2, 
                max=150,
                value = 4
              ),]),
              dbc.FormGroup([
                dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=dt(2019, 1, 1),
                    max_date_allowed=dt(2019, 12, 31),
                    initial_visible_month=dt(2019, 5, 1),
                    date=dt(2019, 5, 1).date(),
                    show_outside_days = False, 
                ),
            ]),
        ]),md=4),
      dbc.Col(html.Div(id="cluster-graph"), md=8)
      ],align="center",)
    ])


@app.callback(
    Output("cluster-graph", "children"),
    [
        dash.dependencies.Input('my-date-picker-single', 'date'),
        Input('age','value')
    ],
)
def make_graph(date_start,age):
  ## it verifies the age firs, if it is a valid age, returns a graph, a warning if not
  print(age)
  if (age == None):
    return html.Div('Seleccione una edad valida')
  fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                             color_continuous_scale="Viridis",
                             range_color=(0, 12),
                             mapbox_style="carto-positron",
                             zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                             opacity=0.5,
                             labels={'unemp':'unemployment rate'}
                            )
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  return dcc.Graph(figure = fig)

def create_app():
  # App settings
  return app