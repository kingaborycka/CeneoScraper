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
        features = {key:extract_feature(opinion,*args)
                    for key, args in selectors.items() }
        features['opinion_id'] = int(opinion['data-entry-id'])
        features['purchased'] = True if features['purchased'] =='Opinia potwierdzona zakupem' else False
        features['useful'] = int(features['useful'])
        features['useless'] = int(features['useless'])
        features['content'] = remove_whitespaces(features['content'])
        features['pros'] = remove_whitespaces(features['pros'])
        features['cons'] = remove_whitespaces(features['cons'])
    
        opinions_list.append(features)
    
    try:
        url = url_prefix + page_tree.select('a.pagination__next').pop()['href']
    except IndexError:
        url = None
    
    print('url',url)
    

# tworzenie pliku json
with open('opinions/'+product_id + '.json','w', encoding = 'UTF-8') as fp:
    json.dump(opinions_list, fp, ensure_ascii=False, separators=(',',':'), indent = 4)




