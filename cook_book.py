# coding: utf-8

#  Create cook book
# data = "Омлет\n3\nЯйца | 2 | шт\nМолоко | 50 | мл\nПомидор | 100 | г\nКаша\n2\nМолоко | 200 | мл\nКрупа | 100 | мл"
# # with open('recepts.txt', 'w', encoding='utf8') as myfile:
#     myfile.write(data)
import re


def download_cook_book():
    regex1 = r"(?P<recep>[а-яА-Я]+\n)(?P<num_ing>[0-9]+\n)"
    regex2 = "((?P<ing>\w+) \| (?P<amn>\S+) \| (?P<unt>\w+))"
    patern1 = re.compile(regex1, flags=re.MULTILINE)
    patern2 = re.compile(regex2, flags=re.MULTILINE)
    with open('recepts.txt', 'r', encoding='utf8') as myfile:
        data = myfile.read()
    cook_list = dict()
    for match1 in patern1.finditer(data):
        m_end = match1.end()
        recep_name = match1.group('recep').lower().strip()
        n_ingr = int(match1.group('num_ing'))
        ingr_list = list()
        for _, match2 in zip(range(n_ingr), patern2.finditer(data[m_end:])):
            ingr_list.append([match2.group('ing'), match2.group('amn'), match2.group('unt')])
        cook_list[recep_name] = (n_ingr,ingr_list)
    return cook_list


def prepare_shop_list(book, key, N):
    n_ingr = book[key][0]
    ingr_list = book[key][1]
    print ("На {} порций {} вам надо купить следующие {} продукта:".format(N, key, n_ingr ) )
    for ing in ingr_list:
        print (ing[0], int(ing[1])*N, ing[2])


def main():
    cook_book = download_cook_book()
    print ("Загружено рецептов: {}".format(len(cook_book)) )

    while True :
        name = input("Введите блюдо и кол-во порций (ппц - конец работы): ")
        if 'ппц' in name :
            break
        try:
            name, amount = name.lower().split()
            amount = int(amount)
        except (ValueError) :
            print("повторите ввод: 'блюдо <кол-во порций>'")
        else:
            if name in cook_book.keys():
                prepare_shop_list(cook_book, name, amount )
            else:
                print("нет такого блюда")


if __name__ == "__main__":
    main()
