import os
import json
import requests
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from urllib.parse import unquote
from app.premier_selector import players_data

DATA_DIR = "fpl_data"

# Function to fetch data from the FPL API and save it to a file
def fetch_and_save_data(endpoint, filename):
    url = f"https://fantasy.premierleague.com/api/{endpoint}/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        existing_data.update(data)
        data = existing_data
    with open(filepath, 'w', encoding='utf-8') as f:
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
    fetch_and_save_data(endpoint, filename)
    data = load_data_from_file(filename)
    return data

# Function to get season data for a player
def load_player_stats(player_name):
    player_name = unquote(player_name)
    player_id = next((int(player['id']) for player in players_data if player['web_name'] == player_name), None)
    filename = f"player_{player_id}_fixtures.json"
    data = fetch_data(f"element-summary/{player_id}", filename)
    player_statistics = data['history'] if data else []

    if player_statistics:
        return generate_player_stats(player_statistics, player_name, player_id)
    else:
        print(f"Player '{player_name}' data not found or error loading data.")
        return html.Div(f"No valid data found for player '{player_name}'.")

def generate_player_stats(player_stats, player_name, player_id):
    try:
        # Extract relevant stats
        gameweeks = [entry['round'] for entry in player_stats]
        points = [entry['total_points'] for entry in player_stats]
        goals_scored = [entry['goals_scored'] for entry in player_stats]
        assists = [entry['assists'] for entry in player_stats]
        bonus_points = [entry['bonus'] for entry in player_stats]
        clean_sheets = [entry['clean_sheets'] for entry in player_stats]

        # Fetch player position
        player_position = next((player['element_type'] for player in players_data if player['id'] == player_id), None)

        # Customize visualization based on player position
        if player_position == 1:  # Goalkeeper
            # Customize visualization for goalkeeper
            saves = [entry['saves'] for entry in player_stats]
            penalties_saved = [entry['penalties_saved'] for entry in player_stats]

            # Create traces for goalkeeper
            saves_trace = go.Scatter(x=gameweeks, y=saves, mode='lines+markers', name='Saves', marker=dict(color='purple'), line=dict(shape='spline'))
            penalties_saved_trace = go.Scatter(x=gameweeks, y=penalties_saved, mode='lines+markers', name='Penalties Saved', marker=dict(color='orange'), line=dict(shape='spline'))
            clean_sheets_trace = go.Scatter(x=gameweeks, y=clean_sheets, mode='lines+markers', name='Clean Sheets', marker=dict(color='blue'), line=dict(shape='spline'))
            bonus_points_trace = go.Scatter(x=gameweeks, y=bonus_points, mode='lines+markers', name='Bonus Points', marker=dict(color='green'), line=dict(shape='spline'))
            points_trace = go.Scatter(x=gameweeks, y=points, mode='lines+markers', name='GW Points', marker=dict(color='red'), line=dict(shape='spline'))

            # Update layout
            layout = go.Layout(
                title=f"Performance of {player_name} (Goalkeeper) in the 2023/24 season",
                xaxis=dict(title='Gameweeks'),
                yaxis=dict(title='Stats'),
                # legend=dict(orientation='h'),
                plot_bgcolor='rgba(255, 228, 196, 0.9)',
                paper_bgcolor='rgba(47, 79, 79, 0.3)',
                margin=dict(l=40, r=40, t=50, b=40)
            )

            # Create figure
            fig = go.Figure(data=[saves_trace, penalties_saved_trace, clean_sheets_trace, bonus_points_trace, points_trace], layout=layout)

        elif player_position == 2:  # Defender
            # Customize visualization for defender

            # Create traces for defender
            clean_sheets_trace = go.Scatter(x=gameweeks, y=clean_sheets, mode='lines+markers', name='Clean Sheets', marker=dict(color='blue'), line=dict(shape='spline'))
            assists_trace = go.Scatter(x=gameweeks, y=assists, mode='lines+markers', name='Assists', marker=dict(color='green'), line=dict(shape='spline'))
            goals_scored_trace = go.Scatter(x=gameweeks, y=goals_scored, mode='lines+markers', name='Goals Scored', marker=dict(color='red'), line=dict(shape='spline'))
            bonus_points_trace = go.Scatter(x=gameweeks, y=bonus_points, mode='lines+markers', name='Bonus Points', marker=dict(color='purple'), line=dict(shape='spline'))
            points_trace = go.Scatter(x=gameweeks, y=points, mode='lines+markers', name='GW Points', marker=dict(color='orange'), line=dict(shape='spline'))

            # Update layout
            layout = go.Layout(
                title=f"Performance of {player_name} (Defender) in the 2023/24 season",
                xaxis=dict(title='Gameweeks'),
                yaxis=dict(title='Stats'),
                # legend=dict(orientation='h'),
                plot_bgcolor='rgba(255, 228, 196, 0.9)',
                paper_bgcolor='rgba(47, 79, 79, 0.3)',
                margin=dict(l=40, r=40, t=80, b=40)
            )

            # Create figure
            fig = go.Figure(data=[clean_sheets_trace, assists_trace, goals_scored_trace, bonus_points_trace, points_trace], layout=layout)

        elif player_position == 3:  # Midfielder
            # Customize visualization for midfielder

            # Create traces for midfielder
            clean_sheets_trace = go.Scatter(x=gameweeks, y=clean_sheets, mode='lines+markers', name='Clean Sheets', marker=dict(color='blue'), line=dict(shape='spline'))
            assists_trace = go.Scatter(x=gameweeks, y=assists, mode='lines+markers', name='Assists', marker=dict(color='green'), line=dict(shape='spline'))
            goals_scored_trace = go.Scatter(x=gameweeks, y=goals_scored, mode='lines+markers', name='Goals Scored', marker=dict(color='red'), line=dict(shape='spline'))
            bonus_points_trace = go.Scatter(x=gameweeks, y=bonus_points, mode='lines+markers', name='Bonus Points', marker=dict(color='purple'), line=dict(shape='spline'))
            points_trace = go.Scatter(x=gameweeks, y=points, mode='lines+markers', name='GW Points', marker=dict(color='orange'), line=dict(shape='spline'))

            # Update layout
            layout = go.Layout(
                title=f"Performance of {player_name} (Midfielder) in the 2023/24 season",
                xaxis=dict(title='Gameweeks'),
                yaxis=dict(title='Stats'),
                # legend=dict(orientation='h'),
                plot_bgcolor='rgba(255, 228, 196, 0.9)',
                paper_bgcolor='rgba(47, 79, 79, 0.3)',
                margin=dict(l=40, r=40, t=80, b=40)
            )

            # Create figure
            fig = go.Figure(data=[clean_sheets_trace, assists_trace, goals_scored_trace, bonus_points_trace, points_trace], layout=layout)

        elif player_position == 4:  # Forward
            # Customize visualization for forward

            # Create traces for forward
            assists_trace = go.Scatter(x=gameweeks, y=assists, mode='lines+markers', name='Assists', marker=dict(color='green'), line=dict(shape='spline'))
            goals_scored_trace = go.Scatter(x=gameweeks, y=goals_scored, mode='lines+markers', name='Goals Scored', marker=dict(color='red'), line=dict(shape='spline'))
            bonus_points_trace = go.Scatter(x=gameweeks, y=bonus_points, mode='lines+markers', name='Bonus Points', marker=dict(color='purple'), line=dict(shape='spline'))
            points_trace = go.Scatter(x=gameweeks, y=points, mode='lines+markers', name='GW Points', marker=dict(color='orange'), line=dict(shape='spline'))

            # Update layout
            layout = go.Layout(
                title=f"Performance of {player_name} (Forward) in the 2023/24 season",
                xaxis=dict(title='Gameweeks'),
                yaxis=dict(title='Stats'),
                # legend=dict(orientation='h'),
                plot_bgcolor='rgba(255, 228, 196, 0.9)',
                paper_bgcolor='rgba(47, 79, 79, 0.3)',
                margin=dict(l=40, r=40, t=80, b=40)
            )

            # Create figure
            fig = go.Figure(data=[assists_trace, goals_scored_trace, bonus_points_trace, points_trace], layout=layout)

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
            className="d-flex justify-content-center align-items-center vh-70"
        )
    except KeyError:
        return html.Div(f"No valid data found for player '{player_name}'.")