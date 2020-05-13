from app import app
from flask import render_template, request
from flaskext.markdown import Markdown
from app.forms import ProductForm
from app.models import Product, Opinion
import requests

app.config['SECRET_KEY'] = "Tajemniczy_kod"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    content= ''
    with open("README.md",'r') as f:
        content = f.read()
    print(content)
    return render_template('about.html',text=content)

@app.route('/extract', methods=['POST','GET'])
def extract():
    form = ProductForm() 
    if form.validate_on_submit():
        page_response = requests.get("https://www.ceneo.pl/"+request.form['product_code'])
        if page_response.status_code == 200:
            product = Product(request.form['product_code'])
            product.extract_product()
            return "OK"
        else:
            form.product_code.errors.append("Dla podanego kodu nie ma produktu")
            return render_template('extract.html',form=form)
    return render_template('extract.html',form=form)

@app.route('/products')
def products():
    pass
    
@app.route('/prosuct/<product_id>')
def product():    
    return render_template('products.html',)


@app.route('/analyzer/<product_id>')
def analyzer():
    return 'Podaj kod produktu do analizy'