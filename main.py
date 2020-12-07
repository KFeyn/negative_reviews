import re
from PIL import Image
import os

from sel import review_downloader
from text_analyzer import full_preprocessing
from text_analyzer import top_graphics


def processing(link_for_process):

    splitted = link_for_process.split('/')

    if re.search(r'\D', splitted[4]) is None:
        final = splitted[0] + '/' + splitted[1] + '/' + splitted[2] + '/' + splitted[3] + '/' + splitted[4]
    else:
        final = splitted[0] + '/' + splitted[1] + '/' + splitted[2] + '/' + splitted[3] + '/' + \
                splitted[4][:re.search(r'\D', splitted[4]).start()]

    return final


def program(proc_link):
    try:
        review_downloader(proc_link)

    except:
        review_downloader(proc_link)

    text, words, product_name = full_preprocessing('reviews.txt')

    os.remove('reviews.txt')

    for i in range(1, 5):
        if i == 1:
            top_graphics(i, words, product_name)
        else:
            top_graphics(i, text, product_name)

        try:
            file_name = 'freq_' + str(i) + '.png'
            img = Image.open(file_name)
            img.show()
            os.remove(file_name)
        except FileNotFoundError:
            pass


success = False
while not success:
    try:
        link = input()
        if link == 'exit':
            break
        processed_link = processing(link)
        success = True
    except IndexError:
        print('Incorrect link format!')
        pass

if link != 'exit':
    program(processed_link)
else:
    pass


