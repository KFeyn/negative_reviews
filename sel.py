import time
from selenium import webdriver


def review_downloader(product_link):

    # Логинимся в яндексе
    browser = webdriver.Chrome('/Users/feyn/Documents/Мои дурацкие творения/reviews negative/chromedriver')

    login = ''
    password = ''

    login_link = 'https://passport.yandex.ru/auth'

    product_link = product_link

    browser.get(login_link)

    browser.find_element_by_id('passp-field-login').send_keys(login)
    browser.find_element_by_xpath("//button[@type='submit']").click()

    time.sleep(1)

    browser.find_element_by_id('passp-field-passwd').send_keys(password)

    time.sleep(1)

    # Достаем название продукта

    all_troubles = ''

    browser.get(product_link + 'reviews')

    product_name = browser.find_elements_by_tag_name('h1')[0].text
    all_troubles += product_name

    time.sleep(1)

    # Бегаем по страничкам с отзывами и записываем негативные в файл

    for i in range(1, 1000):

        browser.get(product_link + 'reviews?page=' + str(i))

        all_troubles += '\n\n'

        trouble = browser.find_elements_by_xpath("//dt[text()='Недостатки: ']/following-sibling::dd")

        if trouble:
            for j in range(len(trouble)):
                all_troubles += trouble[j].text
                all_troubles += '\n\n'
        else:
            break

        time.sleep(1)

    with open('reviews.txt', 'w') as file:
        file.write(all_troubles)

    browser.quit()

