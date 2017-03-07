# coding: utf-8

#  Create cook book
# data = "Омлет\n3\nЯйца | 2 | шт\nМолоко | 50 | мл\nПомидор | 100 | г\nКаша\n2\nМолоко | 200 | мл\nКрупа | 100 | мл"
# # with open('recepts.txt', 'w', encoding='utf8') as myfile:
#     myfile.write(data)
import re
import pprint as pp
import json
import yaml
import xml.etree.ElementTree as ET


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
    return cook_list


def recepts_to_xml(book):
    xml_start = '<?xml version="1.0" encoding="UTF-8"?>\n<recepts>\n'

    for recept in book.keys():
        num = book[recept][0]
        ingr_list = book[recept][1]
        xml_start += '  <recept name="'+recept+'" numb="'+str(num)+'">\n'
        for ing in ingr_list:
            xml_start += '    <ingr name="'+ing[0]+'" amount="'+ing[1]+'" unit="'+ing[2]+'"></ingr>\n'
        xml_start += '  </recept>\n'

    return xml_start + '</recepts>'


def xml_to_recepts(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    if root.tag != 'recepts' :
        print ("invalid recept file format")
        return None
    cook_list = dict()
    for recept in root:
        recept_name = recept.attrib['name']
        recept_numb = recept.attrib['numb']
        ingr_list = list()
        for ingr in recept:
            ingr_name = ingr.attrib['name']
            ingr_amount = ingr.attrib['amount']
            ingr_unit = ingr.attrib['unit']
            ingr_list.append([ingr_name, ingr_amount, ingr_unit])
        cook_list[recept_name] = [int(recept_numb), ingr_list]

    return cook_list


def main():
    cook_book = download_cook_book()
    print('Загружено из исходного .тхт файла {} рецепта:'.format(len(cook_book)))
    pp.pprint(cook_book)

    with open('recept.json', 'w', encoding='utf-8') as json_file:
        json.dump(cook_book, json_file, indent=2, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    print('\n1) Рецепты записаны в файл: recept.json')
    with open('recept.json', 'r', encoding='utf-8') as json_file:
        data_loaded = json.load(json_file)
    if cook_book == data_loaded:
        print('   Данные загруженные из json файла идентичны исходным\n')
    else:
        print('   Ошибка в формате загруженных данных из json файла\n')

    with open('recept.yaml', 'w', encoding='utf8') as yaml_file:
        yaml.dump(cook_book, yaml_file, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    print('\n2) Рецепты записаны в файл: recept.yaml')
    with open('recept.yaml', 'r', encoding='utf-8') as yaml_file:
        data_loaded = yaml.load(yaml_file)
    if cook_book == data_loaded:
        print('   Данные загруженные из yaml файла идентичны исходным\n')
    else:
        print('   Ошибка в формате загруженных данных из yaml файла\n')

    with open('recept.xml', 'w', encoding='utf8') as xml_file:
        xml_file.write(recepts_to_xml(cook_book))
    print('\n3) Рецепты записаны в файл: recept.xml')
    data_loaded = xml_to_recepts('recept.xml')
    if cook_book == data_loaded:
        print('   Данные загруженные из xml файла идентичны исходным\n')
    else:
        print('   Ошибка в формате загруженных данных из xml файла\n')

if __name__ == "__main__":
    main()
