from flask import Flask, render_template

from app.routes.open_crime_estimation import create_open_estimation_dash_app

server = Flask(__name__)

create_open_estimation_dash_app(server)

@server.route('/')
def index():
	return redirect('https://aml-cs.github.io/')

@server.route('/seconddawork')
def seconddawork():
	return render_template('seconddawork.html', title='Second International Workshop on Data Assimilation for Decision Making, Colombia ')
