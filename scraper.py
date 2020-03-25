#import bibliotek 
import requests 
from bs4 import BeautifulSoup
import pprint
import json

#adres URL strony z opiniami

url_prefix = "https://www.ceneo.pl"
product_id = input('Podaj kod produktu: ')
url_postfix = "#tab=reviews"
url = url_prefix +'/'+product_id + url_postfix
opinions_list = []

#pętla przechodząca przez wszystkie strony z opiniami
while url is not None:

    #pobranie kodu HTML strony z adresu URL
    page_response = requests.get(url)
    page_tree = BeautifulSoup(page_response.text,'html.parser')

    #wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
    opinions = page_tree.select('li.js_product-review')


    for opinion in opinions:
        opinion_id = opinion['data-entry-id']
        author = opinion.select('div.reviewer-name-line').pop().string.strip()
        try:
            recomendation = opinion.select('div.product-review-summary > em').pop().string
        except IndexError:
            recomendation = None
        stars = opinion.select('span.review-score-count').pop().string.strip()
        try:
            purchased = opinion.select('div.product-review-pz').pop().string
        except IndexError:
            purchased = None
        useful = opinion.select('button.vote-yes').pop()['data-total-vote']
        useless = opinion.select('button.vote-no').pop()['data-total-vote']
        content = opinion.select('p.product-review-body').pop().get_text().strip()


        # - wady i zalety
        try:
            cons = opinion.select('div.cons-cell >ul').pop().get_text().strip()
        except IndexError:
            cons = None
        try:
            pros = opinion.select('div.pros-cell >ul').pop().get_text().strip()
        except IndexError:
            pros = None

        date = opinion.select('span.review-time > time')
        review_date = date.pop(0)['datetime']
        try:
            purchase_date = date.pop(0)['datetime']
        except IndexError:
            purchase_date = None

        opinion_dict = {
            'opinion_id': opinion_id,
            'author': author,
            'recomendation':recomendation,
            'stars':stars,
            'content':content,
            'pros': pros,
            'cons': cons,
            'useful': useful,
            'useless': useless,
            'purchased': purchased,
            'purchase_date': purchase_date,
            'review_date': review_date
        }
        opinions_list.append(opinion_dict)
        print('url',url)
    try:
        url = url_prefix + page_tree.select('pagination__next').pop()['href']
    except IndexError:
        url = None

    


# tworzenie pliku json
with open(product_id + '.json','w') as fp:
    json.dump(opinions_list, fp, ensure_ascii=False)





