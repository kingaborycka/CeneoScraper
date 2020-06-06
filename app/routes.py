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
        username = request.form['username']
        if [x for x in users.users if x.username == username]:
            form.error = True
            return render_template('new_account.html',form=form)
        password = request.form['password']
        users.users.append(users.User(id=len(users.users)+1,username=username,password=password))
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
            return render_template('login.html',form=form)
        if user and user.password == password:
            session['user_id'] = user.id
            print(session)
            return redirect(url_for('index'))
        form.error = True
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

@app.route('/product_page/<id>')
def product_page(id):
    print('działa','id:',id)
    product_id_list = [x for x in users.users[session['user_id']-1].products]
    product_id = product_id_list[int(id)]
    return redirect(url_for("product", product_id=product_id))


@app.route('/extract', methods=['POST','GET'])
def extract():
    form = ProductForm() 
    if form.validate_on_submit():
        page_response = requests.get("https://www.ceneo.pl/"+request.form['product_code']+'#tab=reviews')
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
    names,opinions_count,cons_count, pros_count, average_mark = [],[],[],[],[]
    for product in users.users[session['user_id']-1].products.values():
        names.append(product.name)
        opinions_count.append(product.opinions_count)
        cons_count.append(product.cons_count)
        pros_count.append(product.pros_count)
        average_mark.append(product.average_mark)    
    
    products_list = pd.DataFrame.from_records({
        'Nazwa produktu':names,
        'Liczba opinii':opinions_count,
        'Liczba wad': cons_count,
        'Liczba zalet':pros_count,
        'Średnia ocena':average_mark
        }
    )
    products_list = products_list[['Nazwa produktu','Liczba opinii','Liczba wad','Liczba zalet','Średnia ocena']]
    return render_template('products.html', tables=[
        products_list.to_html(
            classes="table table-striped table-bordered", 
            table_id="example",
        )
    ])
    
@app.route('/product/<product_id>')
def product(product_id):  
    product = Product(product_id)
    product.read_product()
    opinions = pd.DataFrame.from_records([opinion.__dict__() for opinion in product.opinions])
    opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))
    user_products = users.users[session['user_id']-1].products
    if product_id not in user_products.keys(): 
        user_products[product_id] = product
        print('Produkt. liczba opinii:',product.opinions_count)
    return render_template('product.html', tables=[
        opinions.to_html(
            classes="table table-striped table-bordered", 
            table_id="example",
        )
    ], name = product.name)



@app.route('/analyzer/<product_id>')
def analyzer():
    return 'Podaj kod produktu do analizy'