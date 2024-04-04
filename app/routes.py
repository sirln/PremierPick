from app import app
from datetime import datetime
from flask import render_template, send_from_directory

# from app.dash_layout import generate_player_page

@app.route('/')
@app.route('/index')
def index():
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%d-%m')
    current_year = datetime.now().strftime('%Y')
    return render_template('index.html', now=current_time, today=current_date, year=current_year)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images','favicon.ico')


# @app.route('/player/<player_name>')
# def player_page(player_name):
#     player_page_html = generate_player_page(player_name)
#     return render_template('player.html', player_page_html=player_page_html)