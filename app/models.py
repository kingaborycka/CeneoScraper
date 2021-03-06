from app import app
from app.utils import extract_feature, remove_whitespaces
import requests
from bs4 import BeautifulSoup
from enum import Enum, auto
import json

class Product:
    def __init__(self, product_id = None, name = None, opinions=[]):
        self.product_id = product_id
        self.name = name
        self.opinions = opinions
        self.cons_count=0
        self.pros_count=0
        self.stars_count=0
        self.average_mark=None
        self.opinions_count = 0
        
    
    def extract_product(self):
        page_response = requests.get("https://www.ceneo.pl/"+ self.product_id)
        page_tree = BeautifulSoup(page_response.text,'html.parser')
        self.name = page_tree.select("h1.product-name").pop().get_text().strip()
        try:
            self.opinions_count = int(page_tree.select("a.product-reviews-link > span").pop().get_text().strip())
        except:
            pass
        if self.opinions_count > 0:
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
                for opinion in opinions:
                    op = Opinion()
                    op.extract_opinion(opinion)
                    op.transform_opinion()
                    opinions_list.append(op)
                    try:
                        if op.cons:
                            print(op.cons)
                            self.cons_count += 1
                            print(self.cons_count)
                    except AttributeError:
                        pass
                    try:
                        if op.pros:
                            self.pros_count += 1
                    except AttributeError:
                        pass
                    try:
                        self.stars_count += float(op.stars.split('/')[0].replace(',','.'))
                    except:
                        pass
                try:
                    url = url_prefix + page_tree.select('a.pagination__next').pop()['href']
                except IndexError:
                    url = None
            self.opinions = opinions_list  
        else:
            opinions_list = []
            opinions_list.append(Opinion('',None,None,'0/5',None,0,0))
            self.opinions = opinions_list
            print('Nie ma opinii')
        try:
            self.average_mark = round(self.stars_count/self.opinions_count,1)
        except:
            self.average_mark = 'Brak'
        print('Ilość opinii:',self.opinions_count)  

    def __str__(self):
        return f'product_id: {self.product_id}\n nazwa: {self.name}\n\n'+'\n'.join(str(opinion) for opinion in self.opinions)
    def __dict__(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "opinions_count": self.opinions_count,
            "cons_count": self.cons_count,
            "pros_count":self.pros_count,
            "average_mark":self.average_mark,
            "opinions": [opinion.__dict__() for opinion in self.opinions]
        }

    def save_product(self):
        with open("app/opinions/"+self.product_id+".json",'w',encoding="UTF-8") as fp:
            json.dump(self.__dict__(),fp, ensure_ascii=False,separators=(',',':'),indent=4)
    
    def read_product(self): 
        pr = json.load(open("app/opinions/"+self.product_id+".json", 'r', encoding='utf-8'))
        print(pr)
        
        self.name = pr['name']
        opinions = pr['opinions']
        self.opinions = []
        self.opinions_count = pr['opinions_count']
        self.cons_count = pr['cons_count']
        self.pros_count = pr['pros_count']
        self.average_mark = pr['average_mark']
        for opinion in opinions:
            op = Opinion(**opinion)
            self.opinions.append(op)


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
        return '\n'.join(key+': '+('' if getattr(self,key) is None else str(getattr(self,key))) for key in self.selectors.keys())
        # return f'opinion_id: {self.opinion_id}\nauthor: {self.author}\nrecommendation: {self.recommendation}\nstars: {self.stars}\ncontent: {self.content}\n{self.pros}\n{self.cons}\nuseful: {self.useful}\nuseless: {self.useless}\npurchased: {self.purchased}\npurchase_date: {self.purchase_date}\nreview_date: {self.review_date}\n'

    def __dict__(self):
        features = {key:('' if getattr(self,key) is None else getattr(self,key))
                    for key in self.selectors.keys()}
        features['opinion_id'] = self.opinion_id
        return features
    
    def extract_opinion(self,opinion):
        for key, args in self.selectors.items():
            setattr(self, key, extract_feature(opinion, *args))
        #self.author = extract_feature(opinion, *self.selectors['author'])
        self.opinion_id = int(opinion['data-entry-id'])

    def transform_opinion(self):
        self.purchased = True if self.purchased =='Opinia potwierdzona zakupem' else False
        self.useful = int(self.useful)
        self.useless = int(self.useless)
        self.content = remove_whitespaces(self.content)
        try:
            self.pros = remove_whitespaces(self.pros).replace('Zalety.','')
        except AttributeError:
            pass
        try:
            self.cons = remove_whitespaces(self.cons).replace('Wady.','')
        except AttributeError:
            pass

    def from_dict(self, opinion_dict):
        for key, value in opinion_dict.items():
            setattr(self, key, value)

