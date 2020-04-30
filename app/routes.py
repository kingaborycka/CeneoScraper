from app import app
from flask import render_template, request
from flaskext.markdown import Markdown
from app.forms import ProductForm
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

@app.route('/extract')
def extract():
    print(request.method)
    if request.method == "POST":
        return "Przesłano formularz"     
    form = ProductForm()
    return render_template('extract.html',form=form)

@app.route('/products')
def products():
    return render_template('products.html',)


@app.route('/analyzer/<product_id>')
def analyzer():
    return 'Podaj kod produktu do analizy'