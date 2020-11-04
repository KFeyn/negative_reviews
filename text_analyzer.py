from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from catboost.text_processing import Dictionary
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from matplotlib.ticker import MaxNLocator

sns.set()


# Подготавливаем текст
def full_preprocessing(file):

    # Открываем файл и записываем отзывы в строку, отдельно запоминаем название товара
    reviews_file = open(file, 'r')

    reviews_string = ''

    for st in reviews_file:
        reviews_string += st

    reviews_list = reviews_string.split('\n\n')[:-1]
    product_name = reviews_list[0]
    reviews_list = reviews_list[1:-1]


    # Создаем лемматизатор
    my_stem = Mystem()
    russian_stopwords = stopwords.words("russian")

    # Функция препроцессинга
    def preprocess_text(text):
        tokens = my_stem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]
        return tokens

    preprocessed_reviews = [preprocess_text(review) for review in reviews_list]

    return preprocessed_reviews, product_name


# Рисуем частоту биграмм
def top_graphics(gramm, text, product_name):

    # Создаем словари
    dictionary_bigramm = Dictionary(occurence_lower_bound=2, max_dictionary_size=10, gram_order=gramm)
    dictionary_bigramm.fit(text);
    dictionary_bigramm.save('dictionary.txt')

    # Cчитываем статистику из файла
    file = open('dictionary.txt', 'r').readlines()
    name = list()
    freq = list()
    for i in range(2, len(file)):
        freq.append(int(file[i].split('\t')[1]))
        name.append(file[i].split('\t')[2][:-1])

    # Удаляем файл
    os.remove("dictionary.txt")

    # Создаем и сортируем датафрейм
    frame = pd.DataFrame({'Name': name, 'Frequency': freq})
    frame = frame.sort_values('Frequency', ascending=True)

    # Создаем градиент по цвету и рисуем
    my_colors = [(x / 20.0, x / 10.0, 0.1) for x in range(len(frame), 0, -1)]

    ax = plt.figure(figsize=(20, 10)).gca()
    ax.barh('Name', 'Frequency', data=frame, color=my_colors)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title(f"Негативные тенденции товара {product_name}", fontsize=30, verticalalignment='bottom')
    ax.set_xlabel("Количество упоминаний", fontsize=20)
    plt.savefig(f'freq_{gramm}.png')
