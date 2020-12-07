import re
from PIL import Image

from sel import review_downloader
from text_analyzer import full_preprocessing
from text_analyzer import top_graphics


# link = 'https://market.yandex.ru/product--vneshnii-hdd-toshiba-canvio-ready-1-tb/13043839?track=tabs'

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

    # os.remove('reviews.txt')
    #
    top_graphics(1, words, product_name)
    top_graphics(2, text, product_name)
    top_graphics(3, text, product_name)
    # top_graphics(4, text, product_name)

    img = Image.open('freq_1.png')
    img2 = Image.open('freq_2.png')
    img3 = Image.open('freq_3.png')
    img.show()
    img2.show()
    img3.show()


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



