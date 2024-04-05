from flask import Flask
from dash import Dash, callback_context
from dash_bootstrap_components import themes
from app.dash_layout import create_dash_layout


# Initializing the  Flask App and Dash App
app = Flask(__name__)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

# dash_app = Dash(__name__, server=app, url_base_pathname='/dash/', external_stylesheets=[themes.VAPOR])
dash_app = Dash(__name__, server=app, url_base_pathname='/', external_stylesheets=[themes.VAPOR])

# Suppress exception for missing component IDs
dash_app.config.suppress_callback_exceptions = True

# Create Dash layout
create_dash_layout(dash_app)

# Import routes module to ensure the routes are registered
from app import routes