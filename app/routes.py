from app import app
from flask import render_template, request, redirect,url_for, session
from flaskext.markdown import Markdown
from app.forms import ProductForm, LoginForm, AccountForm
from app.models import Product, Opinion
from app import utils, users
import requests
import pandas as pd



app.config['SECRET_KEY'] = "Tajemniczy_kod"

Markdown(app)

@app.route('/')
@app.route('/start')
def layout():
    return render_template('start.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/new_account',methods=['GET','POST'])
def new_account():
    form = AccountForm()
    if request.method == 'POST' and form.validate_on_submit():
        print('dane dobre')
        username = request.form['username']
        if [x for x in users.users if x.username == username]:
            form.error = True
            return render_template('new_account.html',form=form)
        password = request.form['password']
        users.users.append(users.User(id=len(users.users),username=username,password=password))
        return redirect(url_for('accepted'))
    return render_template('new_account.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm() 
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users.users if x.username == username][0]
        except:
            form.error = True
            print('False')
            return render_template('login.html',form=form)
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        form.error = True
        print('False')
        return render_template('login.html',form=form)
    return render_template('login.html',form=form)

@app.route('/accepted')
def accepted():
    return render_template('accepted.html')

@app.route('/about')
def about():
    content = ""
    with open("README.md", "r",encoding="UTF-8") as f:
        content = f.read()
    return render_template("about.html", text=content)

@app.route('/extract', methods=['POST','GET'])
def extract():
    form = ProductForm() 
    if form.validate_on_submit():
        page_response = requests.get("https://www.ceneo.pl/"+request.form['product_code'])
        if page_response.status_code == 200:
            product = Product(request.form['product_code'])
            product.extract_product()
            product.save_product()
            return redirect(url_for("product", product_id=product.product_id))
        else:
            form.product_code.errors.append("Dla podanego kodu nie ma produktu")
            return render_template('extract.html',form=form)
    return render_template('extract.html', form=form)
    

@app.route('/products')
def products():
    pass
    
@app.route('/product/<product_id>')
def product(product_id):  
    product = Product(product_id)
    product.read_product()
    opinions = pd.DataFrame.from_records([opinion.__dict__() for opinion in product.opinions])
    opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))
    return render_template('product.html', tables=[
        opinions.to_html(
            classes="table table-striped table-sm table-responsive",
            table_id='opinions'
        )
    ])



@app.route('/analyzer/<product_id>')
def analyzer():
    return 'Podaj kod produktu do analizy'