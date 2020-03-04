# CeneoScraper
# Faza I - pobranie pojedynczej opinii
- opinia: li.review-box
- identyfikator: li.review-box["data-entry-id"]
- autor: div-review-name-line
- rekomendacja: .product-review-sumary > em
- liczba gwiazdek: span.review-score-count
- czy potwierdzina zakupem: div.product-review-pz
- data wystawienia: time['datetime']
- data zakupu: time['datetime']
- przydatna: button.vote-yes['data-total-vote']
- nieprzydatna: button.vote-no['data-total-vote']
- treść: p.product-review-body
- wady: div.cons-cell > ul
- zalety: div.pros-cell > ul
