from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from catboost.text_processing import Dictionary
import seaborn as sns
import pandas as pd
import os


sns.set()


# Подготавливаем текст
def full_preprocessing(file):

    # Добавляем ломающие символы

    punctuation_upd = punctuation + '»' + '«'

    # Открываем файл и записываем отзывы в строку, отдельно запоминаем название товара
    reviews_file = open(file, 'r')

    reviews_string = ''

    for st in reviews_file:
        reviews_string += st

    reviews_list = reviews_string.split('\n\n')[:-1]
    product_name = reviews_list[0]
    reviews_list = reviews_list[1:]

    # Создаем лемматизатор
    my_stem = Mystem()

    russian_stopwords = stopwords.words("russian")

    russian_stopwords.append('весь')
    russian_stopwords.append('это')
    russian_stopwords.append('очень')
    russian_stopwords.append('хотя')
    russian_stopwords.append('который')
    russian_stopwords.remove('нет')

    russian_stopwords_one = russian_stopwords.copy()

    russian_stopwords.remove('не')
    russian_stopwords.remove('больше')
    russian_stopwords.remove('перед')
    russian_stopwords.remove('никогда')
    russian_stopwords.remove('иногда')
    russian_stopwords.remove('нельзя')
    russian_stopwords.remove('между')
    russian_stopwords.remove('вдруг')

    # Функция препроцессинга
    def preprocess_text(text, russian_stopwords):

        tokens = my_stem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation_upd]
        return tokens

    preprocessed_reviews = [preprocess_text(review, russian_stopwords) for review in reviews_list]
    preprocessed_reviews_word = [preprocess_text(review, russian_stopwords_one) for review in reviews_list]

    return preprocessed_reviews, preprocessed_reviews_word, product_name


# Рисуем частоту биграмм
def top_frame(gramm, text, product_name):

    # Создаем словари
    dictionary = Dictionary(occurence_lower_bound=2, max_dictionary_size=10, gram_order=gramm)
    dictionary.fit(text)
    dictionary.save('dictionary.txt')

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

    return frame, product_name


