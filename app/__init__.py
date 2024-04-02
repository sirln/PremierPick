from dash import Dash
from app.dash_layout import create_dash_layout
from flask import Flask, render_template


app = Flask(__name__)
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')

@dash_app.server.route('/dash')
def render_dashboard():
    return render_template('dash.html')

create_dash_layout(dash_app)

from app import routes