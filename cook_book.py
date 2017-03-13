# coding: utf-8

#  Create cook book
# data = "Омлет\n3\nЯйца | 2 | шт\nМолоко | 50 | мл\nПомидор | 100 | г\nКаша\n2\nМолоко | 200 | мл\nКрупа | 100 | мл"
# # with open('recepts.txt', 'w', encoding='utf8') as myfile:
#     myfile.write(data)
import re


def download_cook_book():
    patern1 = re.compile(r"(?P<recep>\w+)\s(?P<num_ing>\d+)\s")
    patern2 = re.compile(r"((?P<ing>\w+)\s\|\s(?P<amn>\S+)\s\|\s(?P<unt>\w+))")
    with open('recepts.txt', 'r', encoding='utf8') as file:
        data = file.read().lower()
    cook_list = dict()
    for match1 in patern1.finditer(data):
        ingr_list = list()
        for _, match2 in zip(range(int(match1.group('num_ing'))), patern2.finditer(data[match1.end():])):
            ingr_list.append([match2.group('ing'), match2.group('amn'), match2.group('unt')])
        cook_list[match1.group('recep')] = [int(match1.group('num_ing')), ingr_list]

    print("Загружено рецептов: {}".format(len(cook_list)))
    return cook_list


def user_requests(book):

    def prepare_shop_list(book, key, n):
        n_ingr = book[key][0]
        ingr_list = book[key][1]
        print("На {} порций {} вам надо купить следующие {} продукта:".format(n, key, n_ingr))
        for ing in ingr_list:
            print(ing[0], int(ing[1]) * n, ing[2])

    while True:
        name = input("Введите блюдо и кол-во порций (ппц - конец работы): ").lower()
        if name.strip() == 'ппц':
            break
        try:
            name, amount = name.split()
            amount = int(amount)
        except ValueError:
            print("повторите ввод: 'блюдо <кол-во порций>'")
        else:
            if name in book.keys():
                prepare_shop_list(book, name, amount)
            else:
                print("нет такого блюда")


def main():

    user_requests(download_cook_book())

if __name__ == "__main__":
    main()
