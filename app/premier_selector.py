import os
import json
import requests
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from app.player_form_calculator import fetch_last_7_fixtures, DATA_DIR

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
def load_data_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Parse JSON data
        return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise IOError(f"Error loading data from {filepath}: {e}")

# Function to fetch player data from FPL API
def fetch_player_data():
    filename = "player_data.json"
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        data = load_data_from_file(filepath)
        if data is not None:
            return data
    
    # If file doesn't exist or loading from file fails, fetch data from API
    try:
        data = fetch_and_save_data("bootstrap-static", filename)
        return data
    except IOError as e:
        print(f"Error fetching player data: {e}")
        return None

# Function to fetch team data from FPL API
def fetch_team_data():
    filename = "team_data.json"
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        data = load_data_from_file(filepath)
        if data is not None:
            return data
    try:
        data = fetch_and_save_data("fixtures", filename)
        return data
    except IOError as e:
        print(f"Error fetching team data: {e}")
        return None

# Function to fetch club name based on team ID
def fetch_club_name(team_id, teams):
    for team in teams:
        if team['id'] == team_id:
            return team['name']
    return "Unknown Club"

# Function to calculate form score
def calculate_form_score(player_id):
    fixtures = fetch_last_7_fixtures(player_id)
    # Calculate form score based on fixtures
    return sum(fixture['total_points'] for fixture in fixtures) / 7

# Fetch player data from FPL API
data = fetch_player_data()

# Convert JSON to DataFrame
players_data = data.get('elements', [])  # Use get() to handle missing keys

# Fetch team data
teams = data.get('teams', [])
team_data = fetch_team_data()

# Create DataFrame for training the model
df = pd.DataFrame(players_data)

# Calculate form score for each player
df['form_score'] = df['id'].apply(calculate_form_score)

# Define features and target variable
X = df[['form_score']]
y = df['form_score']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train RandomForestRegressor model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Function to predict player form using the trained model
def predict_player_form(player_data, model):
    features = [[player_data['form_score']]]
    return model.predict(features)[0]

# Sample Player class to hold player data and form score
class Player:
    def __init__(self, id, name, element_type, form, points, club, value):
        self.id = id
        self.name = name
        self.element_type = label_position(element_type)
        self.form = form
        self.points = points
        self.club = club
        self.value = value

# Function to label each position
def label_position(position_id):
    if position_id == 1:
        return "Goalkeeper"
    elif position_id == 2:
        return "Defender"
    elif position_id == 3:
        return "Midfielder"
    elif position_id == 4:
        return "Forward"
    else:
        return "Unknown Position"

# Create list of Player objects
players = []
for player_data in players_data:
    player_id = player_data['id']
    player_name = player_data['web_name']
    element_type = player_data['element_type']
    form = calculate_form_score(player_id)
    points = player_data['total_points']
    club = fetch_club_name(player_data['team'], teams)
    value = player_data['now_cost']
    player = Player(player_id, player_name, element_type, form, points, club, value)
    players.append(player)

# Function to select players for each position based on form
def select_players(position_id, num_players, players):
    position_players = [player for player in players if player.element_type == label_position(position_id)]
    position_players.sort(key=lambda x: x.form, reverse=True)
    position_players = position_players[:num_players]
    return position_players

# Select players for each position
goalkeepers = select_players(1, 10, players)
defenders = select_players(2, 12, players)
midfielders = select_players(3, 12, players)
forwards = select_players(4, 10, players)

