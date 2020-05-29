from app import app
from flask import render_template, request, redirect,url_for, session
from flaskext.markdown import Markdown
from app.forms import ProductForm, LoginForm
from app.models import Product, Opinion
from app import utils, users
import requests



app.config['SECRET_KEY'] = "Tajemniczy_kod"

Markdown(app)

@app.route('/')
@app.route('/start')
def layout():
    return render_template('start.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/new_account')
def new_account():
    return render_template('new_account.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm() 
    if request.method == 'POST':
        print('jest')
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users.users if x.username == username][0]
        except:
            return render_template('login.html',form=form)
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return redirect(url_for('login',form=form))
    return render_template('login.html',form=form)

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
    product = Product()
    print(product.read_product(product_id))
    return render_template('product.html',)



@app.route('/analyzer/<product_id>')
def analyzer():
    return 'Podaj kod produktu do analizy'