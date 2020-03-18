#import bibliotek 
import requests 
from bs4 import BeautifulSoup

#adres URL strony z opiniami

url = "https://www.ceneo.pl/17810145#tab=reviews_scroll"

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

    print(opinion_id,author, recomendation, stars, content, pros, cons, useful, useless, purchased, purchase_date, review_date)



# opinia: li.review-box
# - identyfikator: data-entry-id
# - autor: div-review-name-line
# - rekomendacja: divj.product-review-sumary > em
# - liczba gwiazdek: span.review-score-count
# - czy potwierdzina zakupem: div.product-review-pz
# - data wystawienia: time['datetime']
# - data zakupu: time['datetime']
# - przydatna: button.vote-yes['data-total-vote']
# - nieprzydatna: button.vote-no['data-total-vote']
# - treść: p.product-review-body
# - wady: div.cons-cell > ul
# - zalety: div.pros-cell > ul


#ekstrakcja składowych dla pierwszej opinii z listy 