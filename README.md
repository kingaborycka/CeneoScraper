# CeneoScraper
# Faza I - pobranie pojedynczej opinii
- opinia: li.review-box
- identyfikator: li.review-box["data-entry-id"]
- autor: span.user-post__author-name
- rekomendacja: span.user-post__author-recomendation > em
- liczba gwiazdek: span.user-post__score-count
- czy potwierdzina zakupem: div.review-pz
- data wystawienia: time['datetime']
- data zakupu: time['datetime']
- przydatna: button.vote-yes['data-total-vote']
- nieprzydatna: button.vote-no['data-total-vote']
- treść: div.user-post__text
- wady: div.review-feature__col:has(div.review-feature__title--negatives)
- zalety: div.review-feature__col:has(div.review-feature__title--positives)
# Etap 2 - pobranie wszystkich opinii z pojedynczej strony
- zapis składotych opinii do złożonej struktury danych
- Etap 3 - pobranie wszystkich opinii o pojedynczym produkcie
- sposób przechodzenia po kolejnych stronach z opiniami
- eksport opinii do pliku (.csv lub .xlsx lub .json)
- Etap 4 -
- eliminacja powtarzających się fragmentów kodu
- transformacja danych (typ danych, czyszczenie danych)
- Etap 5 - analiza pobranych danych
- zapis pobranych danych do obiektu dataframe (ramka danych)
- wykonamie prostych obliczeń na danych
- wykonanie prostych wykresów
- Etap 6 - interfejs webowy aplikacji (framework Flask)
- zainstalowanie i uruchamianie Flask'a
- struktura aplikacji 
>/CeneoScraper
>>/run.py
>>/config.py
>>/app
>>>/init.py 
>>>/analyzer.py 
>>>/forms.py
>>>/routes.py
>>>/models.py
>>>/utils.py
>>>/static/
>>>>/main.css 
>>>>/figures/ 
>>>>>/fig.png 
>>>/templates/
>>>>/base.html
>>>/opinions 
>>/requirements.txt
>>/.venv 
>>/README.md
- routing (nawigowanie po stronach serwisu)
- widoki (Jinja)
************************************************************
#IN TERMINAL:
- .venv/Scripts/activate 
- flask run
************************************************************
