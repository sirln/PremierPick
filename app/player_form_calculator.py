import os
import json
import requests

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

# Function to fetch last 7 fixtures data for a player
def fetch_last_7_fixtures(player_id):
    filename = f"player_{player_id}_fixtures.json"
    data = fetch_data(f"element-summary/{player_id}", filename)
    return data['history'][-10:] if data else []


# Function to calculate goalkeeper form
def calculate_goalkeeper_form(player_id):
    # Fetching last 7 fixtures data for the goalkeeper
    fixtures = fetch_last_7_fixtures(player_id)
    if not fixtures:
        return 0  # No fixtures found, form score is 0
    
    # Initializing variables to store cumulative statistics
    minutes_played = 0
    cleansheets_kept = 0
    bonus_points = 0
    saves_made = 0
    assists = 0
    # opponent_goals_scored = 0
    
    # Calculating cumulative statistics
    for fixture in fixtures:
        minutes_played += fixture['minutes']
        cleansheets_kept += 1 if fixture['clean_sheets'] else 0
        bonus_points += fixture['bonus']
        saves_made += fixture['saves']
        assists += fixture['assists']
        # opponent_goals_scored += fixture['opponent_team_score']
    
    # Calculating form score
    # total_weighted_score = (minutes_played * 0.2) + (cleansheets_kept * 0.3) + (bonus_points * 0.1) + (saves_made * 0.1) + (assists * 0) + (opponent_goals_scored * 0.3)
    total_weighted_score = (minutes_played * 0.2) + (cleansheets_kept * 0.3) + (bonus_points * 0.1) + (saves_made * 0.1) + (assists * 0)
    max_possible_score = (7 * (0.2 + 0.3 + 0.1 + 0.1 + 0))
    form_score = (total_weighted_score / max_possible_score) * 100
    
    return form_score

# Function to calculate defender form
def calculate_defender_form(player_id):
    # Fetching last 7 fixtures data for the defender
    fixtures = fetch_last_7_fixtures(player_id)
    if not fixtures:
        return 0  # No fixtures found, form score is 0
    
    # Initializing variables to store cumulative statistics
    minutes_played = 0
    cleansheets_kept = 0
    bonus_points = 0
    assists = 0
    goals_scored = 0
    # opponent_goals_scored = 0
    # opponent_goals_conceded = 0
    
    # Calculating cumulative statistics
    for fixture in fixtures:
        minutes_played += fixture['minutes']
        cleansheets_kept += 1 if fixture['clean_sheets'] else 0
        bonus_points += fixture['bonus']
        assists += fixture['assists']
        goals_scored += fixture['goals_scored']
        # opponent_goals_scored += fixture['opponent_team_score']
        # opponent_goals_conceded += fixture['team_score']
    
    # Calculating form score
    # total_weighted_score = (minutes_played * 0.2) + (cleansheets_kept * 0.3) + (bonus_points * 0.1) + (assists * 0.1) + (goals_scored * 0.2) + (opponent_goals_scored * 0.2) + (opponent_goals_conceded * 0.2)
    total_weighted_score = (minutes_played * 0.2) + (cleansheets_kept * 0.3) + (bonus_points * 0.1) + (assists * 0.1) + (goals_scored * 0.2)
    max_possible_score = (7 * (0.2 + 0.3 + 0.1 + 0.1 + 0.2 + 0.2 + 0.2))
    form_score = (total_weighted_score / max_possible_score) * 100
    
    return form_score

# Function to calculate midfielder form
def calculate_midfielder_form(player_id):
    # Fetching last 7 fixtures data for the midfielder
    fixtures = fetch_last_7_fixtures(player_id)
    if not fixtures:
        return 0  # No fixtures found, form score is 0
    
    # Initializing variables to store cumulative statistics
    minutes_played = 0
    cleansheets_kept = 0
    bonus_points = 0
    assists = 0
    goals_scored = 0
    # opponent_goals_scored = 0
    # opponent_goals_conceded = 0
    
    # Calculating cumulative statistics
    for fixture in fixtures:
        minutes_played += fixture['minutes']
        cleansheets_kept += 1 if fixture['clean_sheets'] else 0
        bonus_points += fixture['bonus']
        assists += fixture['assists']
        goals_scored += fixture['goals_scored']
        # opponent_goals_scored += fixture['opponent_team_score']
        # opponent_goals_conceded += fixture['team_score']
    
    # Calculating form score
    # total_weighted_score = (minutes_played * 0.2) + (cleansheets_kept * 0.1) + (bonus_points * 0.1) + (assists * 0.2) + (goals_scored * 0.3) + (opponent_goals_scored * 0.2) + (opponent_goals_conceded * 0.2)
    total_weighted_score = (minutes_played * 0.2) + (cleansheets_kept * 0.1) + (bonus_points * 0.1) + (assists * 0.2) + (goals_scored * 0.3)
    max_possible_score = (7 * (0.2 + 0.1 + 0.1 + 0.2 + 0.3 + 0.2 + 0.2))
    form_score = (total_weighted_score / max_possible_score) * 100
    
    return form_score

# Function to calculate forward form
def calculate_forward_form(player_id):
    # Fetching last 7 fixtures data for the forward
    fixtures = fetch_last_7_fixtures(player_id)
    if not fixtures:
        return 0  # No fixtures found, form score is 0
    
    # Initializing variables to store cumulative statistics
    minutes_played = 0
    bonus_points = 0
    assists = 0
    goals_scored = 0
    # opponent_goals_conceded = 0
    
    # Calculating cumulative statistics
    for fixture in fixtures:
        minutes_played += fixture['minutes']
        bonus_points += fixture['bonus']
        assists += fixture['assists']
        goals_scored += fixture['goals_scored']
        # opponent_goals_conceded += fixture['team_score']
    
    # Calculating form score
    # total_weighted_score = (minutes_played * 0.2) + (bonus_points * 0.2) + (assists * 0.2) + (goals_scored * 0.4) + (opponent_goals_conceded * 0.2)
    total_weighted_score = (minutes_played * 0.2) + (bonus_points * 0.2) + (assists * 0.2) + (goals_scored * 0.4)
    max_possible_score = (7 * (0.2 + 0.2 + 0.2 + 0.4 + 0.2))
    form_score = (total_weighted_score / max_possible_score) * 100
    
    return form_score
