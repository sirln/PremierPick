# import requests
# from flask import render_template

# from app import app

# FPL_API_BASE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# @app.route('/')
# @app.route('/index')
# def index():
#     # Fetch player data from FPL API
#     response = requests.get(FPL_API_BASE_URL)
#     if response.status_code == 200:
#         data = response.json()
#         players = data['elements']

#         # Extract relevant player information
#         player_names = [player['web_name'] for player in players]
#         player_points = [player['total_points'] for player in players]

#         return render_template('index.html', title='Home', player_names=player_names, player_points=player_points)
#     else:
#         return 'Failed to fetch player data', 500

# @app.route('/team_of_the_week')
# def team_of_the_week():
#     return render_template('team_of_the_week.html', title='Team of the Week')

# @app.route('/teams')
# def teams():
#     # Fetch team data from the FPL API
#     response = requests.get(FPL_API_BASE_URL)
#     if response.status_code == 200:
#         data = response.json()
#         teams = data['teams']
#         season = data['events'][0]['name']  # Assuming the first event name represents the current season

#         # Extract club names, positions, points, and strengths
#         club_names = [team['name'] for team in teams]
#         positions = [team['position'] for team in teams]
#         points = [team['points'] for team in teams]
#         strengths = [team['strength_overall_home'] for team in teams]

#         return render_template('teams.html', season=season, club_names=club_names, positions=positions, points=points, strengths=strengths)
#     else:
#         return 'Failed to fetch team data', 500

# # Import necessary modules
# # import requests
# # from flask import Flask, render_template

# # # Initialize Flask app
# # app = Flask(__name__)

# # # FPL API base URL
# # FPL_API_BASE_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# # @app.route('/')
# # def index():
# #     # Fetch data from FPL API
# #     response = requests.get(FPL_API_BASE_URL)
# #     if response.status_code == 200:
# #         data = response.json()
# #         elements = data['elements']
        
# #         # Extract required data for analysis
# #         player_names = [element['web_name'] for element in elements]
# #         total_points = [element['total_points'] for element in elements]
# #         form = [element['form'] for element in elements]
# #         now_cost = [element['now_cost'] / 10 for element in elements]  # Convert cost to decimal for display
# #         ownership_percentage = [element['selected_by_percent'] for element in elements]

# #         # Render template with data for visualization
# #         return render_template('index.html', player_names=player_names, total_points=total_points, form=form, now_cost=now_cost, ownership_percentage=ownership_percentage)
# #     else:
# #         return 'Failed to fetch data from FPL API', 500

# # if __name__ == '__main__':
# #     app.run(debug=True)

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_id = request.form['player_id']
        player_data = get_payer_data(player_id)
        return render_template('index.html', player_data=player_data)
    return render_template('index.html')

def get_payer_data(player_id):
    url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
    response = requests.get(url)
    data = json.loadsresponse.json()
    return data

if __name__ == '__main__':
    app.run(debug=True)