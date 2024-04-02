from app import app
from flask import render_template
# from app.dash_layout import app as dash_app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
    # return render_template('index.html', title='Home', dash_url='/dashboard')
