import dash

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime as dt

import app.routes.open_crime_estimation.html_render as render

#Here we load a GeoJSON file containing the geometry information for US counties, where feature.id is a FIPS code.

import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
	counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
				   dtype={"fips": str})

cities = pd.read_csv('app/routes/open_crime_estimation/assets/Dept_Cap.csv')

external_stylesheets = [dbc.themes.DARKLY]

def create_open_estimation_dash_app(server):
    app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets,
        server=server,
        url_base_pathname='/open-crime-estimation/',
        assets_folder='./assets'
    )

    app.title='Open crime estimation'

    app.layout = dbc.Container(fluid=False, children=[
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False),

        # Top
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("AML.png"),
                            id="aml-logo",
                        ),
                        
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            id="logo",
                        )
                    ],
                    className="one-third column",
                ),
            ],
            id="header",
            className="row flex-display",
        ),

        # Content will be rendered in this element
        dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.FormGroup([
                html.Label('Gender'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Male', 'value': 'FEMENINO'},
                        {'label': 'Female', 'value': 'MASCULINO'},
                    ],
                    value='F',
                    id = 'gender',
                ),
                html.Label('Age'),
                dcc.Input(
                    id="age",
                    type="number",
                    placeholder="Age",
                    min=2, 
                    max=150,
                    value=18
                ),
                html.Label('City'),
                dcc.Dropdown(
                        id='city',
                        options= [{'label':x['Departamento']+'-'+x['Capital'][:-5], 'value':x['Departamento']+'-'+x['Capital']} for _,x in cities.iterrows()],
                    value='ATLÁNTICO-BARRANQUILLA',)]
                    ),
                html.Label('Date'),
                    dcc.DatePickerSingle(
                        id='my-date-picker-single',
                        min_date_allowed=dt(2010, 1, 1),
                        max_date_allowed=dt(2019, 12, 31),
                        initial_visible_month=dt(2019, 5, 1),
                        date=dt(2019, 5, 1).date(),
                        show_outside_days = False, 
                    ),
                html.Label('Hour (24h format)'),
                dcc.Input(
                    id="hour",
                    type="number",
                    placeholder="13",
                    min=0, 
                    max=23,
                ),
            ]),md=4),
        dbc.Col(html.Div(id="cluster-graph"), md=8),
        ],align="center"),
        html.Div(
            [
                html.Div([
                    html.P('Made by: Randy Consuegra, Omar Mejía, Elias Niño, Sebastian Racedo, Juan Rodriguez.'),
                    html.P('Email: aml-cs@uninorte.edu.co'),
                ]),
                html.A(
                    html.Button("Code source", id="code-source-btn",),
                    href="https://github.com/AML-CS/open-crime-estimation",
                    target="_blank",
                ),
            ],
            className="one-half column",
            id="footer",
        ),
    ])

    @app.callback(
        Output("cluster-graph", "children"),
        [
            Input('my-date-picker-single', 'date'),
            Input('city','value'),
            Input('gender','value'),
            Input('age','value'),
            Input('hour','value'),
        ],
    )

    def make_graph(date,city,gender,age,hour):
        ## it verifies the age firs, if it is a valid age, returns a graph, a warning if not
        if (age == None or city == None or gender == None or hour == None):
            return html.Div(id="empty-cluster")
        geography = city.split(sep='-')
        print(geography)
        dataPath = geography[1]
        ciudad = geography[1][:-5]
        departamento = geography[0]
        sexo = gender
        edad = age
        date_str = date.split(sep='-')
        mes = int(date_str[1])
        dia = int(date_str[2])
        hora = hour
        path = render.plotDataHTML(render.prepareData(dataPath,departamento,ciudad,sexo,edad,mes,dia,hora),departamento,ciudad)
        return html.Iframe(srcDoc = open(path,'r').read(),width='100%',height=600)
