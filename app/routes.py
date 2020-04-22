from app import app
from flask import render_template
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/scraper')
def scraper():
    return "Podaj kod produktu do pobrania opinii"
@app.route('/analyzer/<product_id>')
def analyzer():
    return 'Podaj kod produktu do analizy'