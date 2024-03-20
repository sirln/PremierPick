import requests
import plotly.graph_objs as go
from flask import render_template

from app import app

#FPL_API_BASE_URL = "https://fantasy.premierleague.com/api/"
FPL_API_BASE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/team_of_the_week')
def team_of_the_week():
    return render_template('team_of_the_week.html', title='Team of the Week')


@app.route('/teams')
def teams():
    # Fetch team data from the FPL API
    response = requests.get(FPL_API_BASE_URL + 'bootstrap-static/')
    if response.status_code == 200:
        data = response.json()
        teams = data['teams']
        season = data['events'][0]['name']  # Assuming the first event name represents the current season
        
        # Extract club names, positions, points, and strengths
        club_names = [team['name'] for team in teams]
        positions = [team['position'] for team in teams]
        points = [team['points'] for team in teams]
        strengths = [team['strength_overall_home'] for team in teams]
        
        # Create bar chart trace for positions
        position_trace = go.Bar(
            x=club_names,
            y=positions,
            name='Position'
        )
        
        # Create bar chart trace for points
        points_trace = go.Bar(
            x=club_names,
            y=points,
            name='Points'
        )
        
        # Create bar chart trace for strengths
        strength_trace = go.Bar(
            x=club_names,
            y=strengths,
            name='Strength'
        )
        
        # Combine traces
        data = [position_trace, points_trace, strength_trace]
        
        # Layout
        layout = go.Layout(
            title='Club Stats - {}'.format(season),
            barmode='group'
        )
        
        # Create figure
        fig = go.Figure(data=data, layout=layout)
        graphJSON = fig.to_json()

        return render_template('teams.html', season=season, graphJSON=graphJSON)
    else:
        return 'Failed to fetch team data', 500