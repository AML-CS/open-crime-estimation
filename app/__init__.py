import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime as dt

import app.html_render as render

#Here we load a GeoJSON file containing the geometry information for US counties, where feature.id is a FIPS code.

import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
	counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
				   dtype={"fips": str})

cities = pd.read_csv('assets/Dept_Cap.csv')

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
							,style ={
							"background-color":"transparent",
							"border":"1px solid #bbb",
							"color":'#ffffff'}),
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
					{'label': 'Femenino', 'value': 'FEMENINO'},
					{'label': 'Masculino', 'value': 'MASCULINO'},
				],
				value='F',
				id = 'sex',
			  ),
			  dcc.Input(
				id="age",
				type="number",
				placeholder="Edad",
				min=2, 
				max=150,
				value = 4
			  ),
			  dcc.Dropdown(options= [{'label':x['Departamento']+'-'+x['Capital'][:-5],
			  	'value':x['Departamento']+'-'+x['Capital']} for _,x in cities.iterrows()],
			  	value='ATLÁNTICO-BARRANQUILLA',id='city')]),
			  dbc.FormGroup([
				dcc.DatePickerSingle(
					id='my-date-picker-single',
					min_date_allowed=dt(2010, 1, 1),
					max_date_allowed=dt(2019, 12, 31),
					initial_visible_month=dt(2019, 5, 1),
					date=dt(2019, 5, 1).date(),
					show_outside_days = False, 
				),
			  dcc.Input(
				id="hour",
				type="number",
				placeholder="Horas (0-23)",
				min=0, 
				max=23
			  ),
			]),
		]),md=4),
	  dbc.Col(html.Div(id="cluster-graph"), md=8)
	  ],align="center",)
	])


@app.callback(
	Output("cluster-graph", "children"),
	[
		Input('my-date-picker-single', 'date'),
		Input('city','value'),
		Input('sex','value'),
		Input('age','value'),
		Input('hour','value'),
	],
)
def make_graph(date,city,sex,age,hour):
	## it verifies the age firs, if it is a valid age, returns a graph, a warning if not
	
	if (age == None or city==None or sex == None or hour == None):
		return html.Div('Llene todos los campos de forma valida')
	geography = city.split(sep='-')
	print(geography)
	dataPath = geography[1]
	ciudad = geography[1][:-5]
	departamento = geography[0]
	sexo = sex
	edad = age
	date_str = date.split(sep='-')
	mes = int(date_str[1])
	dia = int(date_str[2])
	hora = hour
	path = render.plotDataHTML(render.prepareData(dataPath,departamento,ciudad,sexo,edad,mes,dia,hora),departamento,ciudad)
	return html.Iframe(srcDoc = open(path,'r').read(),width='100%',height=600)

def create_app():
  # App settings
  return app