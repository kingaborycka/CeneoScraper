import utils
import requests
from bs4 import BeautifulSoup
from enum import Enum, auto
import json


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
            opinions_list = []
            while url :
                print(url)
                #pobranie kodu HTML strony z adresu URL
                page_response = requests.get(url)
                page_tree = BeautifulSoup(page_response.text,'html.parser')

                #wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
                opinions = page_tree.select('div.js_product-review')
                print(len(opinions))
                for opinion in opinions:
                    op = Opinion()
                    op.extract_opinion(opinion)
                    opinions_list.append(op)
                try:
                    url = url_prefix + page_tree.select('a.pagination__next').pop()['href']
                except IndexError:
                    url = None
                print(len(opinions_list))
            self.opinions = opinions_list
            print(len(self.opinions))    
    def __str__(self):
        return f'product id: {self.product_id}\n nazwa: {self.name}\n\n'+'\n'.join(str(opinion) for opinion in self.opinions)
    def __repr__(self):
        return '{'+ f'product id: {self.product_id}\n nazwa: {self.name}\n\n'+'\n'.join(repr(opinion) for opinion in self.opinions)+'}'
    def save_product(self):
        pass

class Opinion:
    #lista składowych opinii wraz z 
    selectors = {
        "author": ['span.user-post__author-name'],
        "recommendation":['span.user-post__author-recomendation > em'],
        "stars":['span.user-post__score-count'],
        "content": ['div.user-post__text'],
        "pros": ['div.review-feature__col:has(div.review-feature__title--positives)'],
        "cons":['div.review-feature__col:has(div.review-feature__title--negatives)'], 
        "useful":['button.vote-yes', "data-total-vote"],
        "useless":['button.vote-no', "data-total-vote"],
        "purchased":['div.review-pz'],
        "purchase_date":['span.user-post__published > time:nth-of-type(1)',"datetime"],
        "review_date":['span.user-post__published > time:nth-of-type(2)',"datetime"]
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
        return f'opinion id: {self.opinion_id}\nauthor: {self.author}\nrecommendation: {self.recommendation}\nstars: {self.stars}\ncontent: {self.content}\n{self.pros}\n{self.cons}\nuseful: {self.useful}\nuseless: {self.useless}\npurchased: {self.purchased}\npurchase_date: {self.purchase_date}\nreview_date: {self.review_date}\n'

    def __repr__(self):
        opinion = {
            "opinion_id": self.opinion_id,
            "author": self.author,
            "recommendation": self.recommendation,
            "stars" : self.stars,
            "content" : self.content,
            "pros" : self.pros,
            "cons" : self.cons,
            "useful" : self.useful,
            "useless" : self.useless,
            "purchased" : self.purchased,
            "purchase_date" : self.purchase_date,
            "review_date" : self.review_date 
        }
        opinion = '\n'.join(x for x in str(opinion).split(','))
        print(type(opinion))
        
        return opinion
    
    def extract_opinion(self,opinion):
        for key, args in self.selectors.items():
            setattr(self, key, utils.extract_feature(opinion, *args))
        #self.author = extract_feature(opinion, *self.selectors['author'])
        self.opinion_id = int(opinion['data-entry-id'])
        pass

    def transform_opinion(self):
        features['purchased'] = True if features['purchased'] =='Opinia potwierdzona zakupem' else False
        features['useful'] = int(features['useful'])
        features['useless'] = int(features['useless'])
        features['content'] = remove_whitespaces(features['content'])
        features['pros'] = remove_whitespaces(features['pros'])
        features['cons'] = remove_whitespaces(features['cons'])
        pass

opinion = Opinion()

product = Product("79688141")
product.extract_product()
for x in product.opinions:
    print(x)
    print(repr(x))

        

