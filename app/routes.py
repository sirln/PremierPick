from app import app
from datetime import datetime
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%d-%m')
    current_year = datetime.now().strftime('%Y')
    return render_template('index.html', now=current_time, today=current_date, year=current_year)