#import bibliotes
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#wyświetlanie zawartośi katalogu opinions
print(os.listdir('./opinions'))

#wczytanie id produktu, którego opinie będą analizowane
product_id = input("Podaj id produktu:")

opinions = pd.read_json('opinions/'+product_id+'.json')
opinions = opinions.set_index('opinion_id')

opinions['stars'] = opinions['stars'].map(lambda x: float(x.split('/')[0].replace(',','.')))
print(opinions['stars'])

#histogram częstości występowania poszczególnych ocen
stars = opinions['stars'].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)))
fig, ax = plt.subplots()
stars.plot.bar(color = 'lightskyblue')
ax.set_title('Gwiazdki')
ax.set_xlabel('liczba gwiazdek')
ax.set_ylabel('liczba opinii')
plt.savefig('figures/'+product_id+'_bar.png')
plt.close()

#udzieł poszczególnych rekomendacji w ogólnej liczbie opinii
recommendation = opinions['recommendation'].value_counts()
recommendation.plot.pie(label ='',autopct='%1.1f%%',colors=['forestgreen','crimson'])
ax.set_title('Rekomendacje')
plt.savefig('figures/'+product_id+'_pie.png')
plt.close()

average_score = opinions['stars'].mean()
pros = opinions['pros'].count()
cons = opinions['cons'].count()
purchased = opinions['purchased'].sum()

print(average_score,pros,cons,purchased)

stars_purchased = pd.crosstab(opinions['stars'],opinions['purchased'])
print(stars_purchased)

