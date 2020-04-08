#import bibliotes
import os
import pandas as pd
#wyświetlanie zawartośi katalogu opinions

print(os.listdir('./opinions'))

#
product_id = input("Podaj id produktu:")

opinions = pd.read_json('opinions/'+product_id+'.json')
opinions = opinions.set_index('opinion_id')

print(opinions)