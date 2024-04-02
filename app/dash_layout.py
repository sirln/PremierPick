# import dash
# import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from app.premier_selector import goalkeepers, defenders, midfielders, forwards

# # Create Dash application
# dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')


# app.layout = html.Div(
#     children=[
#         html.H1("Premier Pick Dashboard"),
#         html.Div(id='graphs-container')
#     ]
# )


def generate_graphs(players, title):
    return dcc.Graph(
        figure={
            'data': [
                {'x': [player.name for player in players], 'y': [player.form for player in players], 'type': 'bar', 'name': 'Form'},
                {'x': [player.name for player in players], 'y': [player.points for player in players], 'type': 'bar', 'name': 'Total Points'}
            ],
            'layout': {
                'title': title
            }
        }
    )


def create_dash_layout(app):
    app.layout = html.Div(
        children=[
            html.H1("Premier Pick Dashboard"),
            html.Div(id='graphs-container')
        ]
    )

    @app.callback(
        Output('graphs-container', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_layout(n):
        goalkeepers_graph = generate_graphs(goalkeepers, "Goalkeepers Form and Total Points")
        defenders_graph = generate_graphs(defenders, "Defenders Form and Total Points")
        midfielders_graph = generate_graphs(midfielders, "Midfielders Form and Total Points")
        forwards_graph = generate_graphs(forwards, "Forwards Form and Total Points")

        graphs_container = html.Div([
            html.Div(goalkeepers_graph, className='graph-container'),
            html.Div(defenders_graph, className='graph-container'),
            html.Div(midfielders_graph, className='graph-container'),
            html.Div(forwards_graph, className='graph-container')
        ], id='graphs-container')

        return graphs_container
