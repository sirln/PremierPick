import os
import json
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from app.premier_selector import players_data

DATA_DIR = "fpl_data"

# Function to fetch and save data from the FPL API
def fetch_and_save_data(endpoint, filename):
    url = f"https://fantasy.premierleague.com/api/{endpoint}/"
    response = requests.get(url, timeout=10)
    data = response.json()
    
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Function to load data from a file
def load_data_from_file(filename):
    try:
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, FileNotFoundError):
        return None

# Function to fetch data, either from file or API
def fetch_data(endpoint, filename):
    data = load_data_from_file(filename)
    if data is None:
        fetch_and_save_data(endpoint, filename)
        data = load_data_from_file(filename)
    return data

# Function to get season data for a player
def load_player_stats(player_name):
    player_id = next((int(player['id']) for player in players_data if player['web_name'] == player_name), None)
    filename = f"player_{player_id}_fixtures.json"
    data = fetch_data(f"element-summary/{player_id}", filename)
    player_statistics = data['history'] if data else []

    if player_statistics:
        return generate_player_stats(player_statistics, player_name)
    else:
        print(f"Player '{player_name}' data not found or error loading data.")
        return html.Div(f"No valid data found for player '{player_name}'.")

def generate_player_stats(player_stats, player_name):
    try:
        # Extract relevant stats
        gameweeks = [entry['round'] for entry in player_stats]
        total_points = [entry['total_points'] for entry in player_stats]
        goals_scored = [entry['goals_scored'] for entry in player_stats]
        assists = [entry['assists'] for entry in player_stats]

        # Create Plotly traces with smooth lines and markers

        total_points_trace = go.Scatter(x=gameweeks, y=total_points, mode='lines+markers', name='Total Points', marker=dict(color='blue'), line=dict(shape='spline'))
        goals_scored_trace = go.Scatter(x=gameweeks, y=goals_scored, mode='lines+markers', name='Goals Scored', marker=dict(color='green'), line=dict(shape='spline'))
        assists_trace = go.Scatter(x=gameweeks, y=assists, mode='lines+markers', name='Assists', marker=dict(color='red'), line=dict(shape='spline'))

        # Create layout
        layout = go.Layout(
            title=f"Performance of {player_name} in the 2023/24 season",
            xaxis=dict(title='Gameweeks'),
            yaxis=dict(title='Stats'),
            legend=dict(orientation='h'),
            plot_bgcolor = 'rgba(255, 228, 196, 0.9)',
            paper_bgcolor = 'rgba(47, 79, 79, 0.3)',
            margin=dict(l=40, r=40, t=80, b=40)
        )

        # Create figure
        fig = go.Figure(data=[total_points_trace, goals_scored_trace, assists_trace], layout=layout)

        graph_height = 400

        card_body_min_height = graph_height + 50

        # Return the plot as a centered dbc.Card component with interactive elements
        return html.Div(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5(f"Performance of {player_name}", className="card-title")),
                    dbc.CardBody(
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(figure=fig, config={'displayModeBar': False}),
                                style={"minHeight": f"{card_body_min_height}px"}
                            ),
                            className="mt-3 justify-content-center align-items-center"
                        ),
                    ),
                ],
                className="shadow-sm bg-white rounded",
                style={"width": "80%"}
            ),
            className="d-flex justify-content-center align-items-center vh-100"
        )
    except KeyError:
        return html.Div(f"No valid data found for player '{player_name}'.")
