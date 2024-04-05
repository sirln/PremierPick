from app import app, dash_app
from datetime import datetime
from flask import request, render_template, send_from_directory


@app.route('/')
@app.route('/dash/')
@app.route('/index')
def index():
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%d-%m')
    current_year = datetime.now().strftime('%Y')
    return render_template('index.html', now=current_time, today=current_date, year=current_year)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images','favicon.ico')
