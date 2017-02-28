# coding: utf-8


data = "Омлет\n3\nЯйца | 2 | шт\nМолоко | 50 | мл\nПомидор | 100 | г\nКаша\n2\nМолоко | 200 | мл\nКрупа | 100 | мл"

with open('recepts.txt', 'w', encoding='utf8') as myfile:
    myfile.write(data)

with open('recepts.txt', 'r', encoding='utf8') as myfile:
    data=myfile.read()

import re

regex1 = r"(?P<recep>[а-яА-Я]+\n)(?P<num_ing>[0-9]+\n)"
regex2 = r"(?P<name>\w+) | (?P<amount>\S+) | (?P<unit>\w+)"
patern1 = re.compile(regex1, flags=re.MULTILINE)
patern2 = re.compile(regex2, flags=re.MULTILINE)

for match1 in patern1.finditer(data):
    m_start = match1.start()
    m_end = match1.end()
    recep_name = match1.group('recep').strip()
    n_ingr = int(match1.group('num_ing') ) 
    print ( "{} состоит из следующих {} ингредиентов: ".format( recep_name, n_ingr ) )
    for i, match2 in zip(range(n_ingr*3), patern2.finditer(data[m_end:]) ) :
        print (match2.group(0), end=' ') # , match2.group('name'), match2.group('amount'), match2.group('unit') )
        if ((i+1) % 3) == 0 :
            print()
    print("\n")   




