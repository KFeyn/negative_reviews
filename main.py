import os

from sel import review_downloader
from text_analyzer import full_preprocessing
from text_analyzer import top_graphics

link = 'https://market.yandex.ru/product--pylesos-samsung-vc20m25/1721284962/'

#review_downloader(link)

text, product_name = full_preprocessing('reviews.txt')

#os.remove('reviews.txt')

top_graphics(1, text, product_name)
top_graphics(2, text, product_name)
top_graphics(3, text, product_name)


