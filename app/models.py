import requests
from bs4 import BeautifulSoup
from enum import Enum, auto

class Product:
    def __init__(self, product_id = None, name = None, opinions=[]):
        self.product_id = product_id
        self.name = name
        self.opinions = opinions
    
    def extract_product(self):
        page_response = requests.get("https://www.ceneo.pl/"+ self.product_id)
        page_tree = BeautifulSoup(page_response.text,'html.parser')
        self.name = page_tree.select("h1.product-name").pop().get_text().strip()
        try:
            opinions_count = int(page_tree.select("a.product-reviews-link > span").pop().get_text().strip())
        except IndexError:
            opinions_count = 0
        if opinions_count > 0:
            url_prefix = "https://www.ceneo.pl"
            url_postfix = "#tab=reviews"
            url = url_prefix +'/'+ self.product_id + url_postfix
            while url :
                #pobranie kodu HTML strony z adresu URL
                page_response = requests.get(url)
                page_tree = BeautifulSoup(page_response.text,'html.parser')

                #wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
                opinions = page_tree.select('li.js_product-review')

                for opinion in opinions:
                    op = Opinion()
                    op.extract_opinion(opinion)
                    self.opinions.append(op)
    
                try:
                    url = url_prefix + page_tree.select('a.pagination__next').pop()['href']
                except IndexError:
                    url = None
                
        
class Selector(Enum):
    AUTHOR = ['div.reviewer-name-line']

class Opinion:
    #lista składowych opinii wraz z 
    selectors = {
        'author': ['div.reviewer-name-line'],
        'recommendation':['div.product-review-summary > em'],
        'stars':['span.review-score-count'],
        'content':['p.product-review-body'],
        'pros': ['div.pros-cell >ul'],
        'cons': ['div.cons-cell >ul'],
        'useful': ['button.vote-yes','data-total-vote'],
        'useless': ['button.vote-no','data-total-vote'],
        'purchased': ['div.product-review-pz'],
        'purchase_date': ['span.review-time > time:nth-of-type(2)','datetime'],
        'review_date': ['span.review-time > time:nth-of-type(1)','datetime']
    }
    def __init__(self, opinion_id=None, author = None, recommendation=None, stars=None, content=None,
                pros=None, cons=None, useful=None, useless=None, purchased=None, purchase_date=None, review_date=None):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.pros = pros
        self.cons = cons
        self.useful = useful
        self.useless = useless
        self.purchased = purchased
        self.purchase_date = purchase_date
        self.review_date = review_date
    
    def __str__(self):
        return f'opinion id: {self.opinion_id}\nauthor: {self.author}\n'

    def __repr__(self):
        pass
    
    def extract_opinion(self,opinion):
        features = {key:extract_feature(opinion,*args)
                    for key, args in selectors.items() }
        self.opinion_id = int(opinion['data-entry-id'])
        pass

    def transform_opinion(self):
        features['purchased'] = True if features['purchased'] =='Opinia potwierdzona zakupem' else False
        features['useful'] = int(features['useful'])
        features['useless'] = int(features['useless'])
        features['content'] = remove_whitespaces(features['content'])
        features['pros'] = remove_whitespaces(features['pros'])
        features['cons'] = remove_whitespaces(features['cons'])
                
opinion = Opinion()
print(opinion)

product = Product("39562616")
product.extract_product()
        

