import re
from PIL import Image
import os
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt


from sel import review_downloader
from text_analyzer import full_preprocessing
from text_analyzer import top_frame


def processing(link_for_process):

    splitted = link_for_process.split('/')

    if re.search(r'\D', splitted[4]) is None:
        final = splitted[0] + '/' + splitted[1] + '/' + splitted[2] + '/' + splitted[3] + '/' + splitted[4]
    else:
        final = splitted[0] + '/' + splitted[1] + '/' + splitted[2] + '/' + splitted[3] + '/' + \
                splitted[4][:re.search(r'\D', splitted[4]).start()]

    return final


def program(proc_link):

    review_downloader(proc_link)

    text, words, product_name = full_preprocessing('reviews.txt')

    os.remove('reviews.txt')

    all_frames = list()

    for i in range(1, 5):

        if i == 1:
            fr = top_frame(i, words, product_name)
        else:
            fr = top_frame(i, text, product_name)

        if not fr[0].empty:
            all_frames.append(fr[0])

    # Создаем градиент по цвету и рисуем на одной картинке
    length = len(all_frames)

    if length != 0:

        fig, axs = plt.subplots(length, 1, figsize=(length * 20, length * 10), facecolor='w', edgecolor='k')

        if not length == 1:
            axs = axs.ravel()
            fig.subplots_adjust(hspace=0.1)

            for i in range(length):

                frame = all_frames[i]

                my_colors = [(x / len(frame), 0.22, 0) for x in range(len(frame))]

                axs[i].barh('Name', 'Frequency', data=frame, color=my_colors)
                axs[i].xaxis.set_major_locator(MaxNLocator(integer=True))

            fig.suptitle(f"Негативные тенденции товара {fr[1]}", fontsize=length * 15)

        else:
            frame = all_frames[0]
            my_colors = [(x / len(frame), 0.22, 0) for x in range(len(frame))]
            axs.barh('Name', 'Frequency', data=frame, color=my_colors)
            axs.xaxis.set_major_locator(MaxNLocator(integer=True))
            axs.set_title(f"Негативные тенденции товара {fr[1]}", fontsize=length * 20, verticalalignment='bottom')

        plt.savefig(f'freq.png')

        img = Image.open(f'freq.png')
        img.show()
        os.remove(f'freq.png')

    else:
        pass


success = False
while not success:
    try:
        #link = 'https://market.yandex.ru/product--kholodilnik-bosch-kgn39uw22r/676436448?cpa=0'
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
