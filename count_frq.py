import json
from xml.dom import minidom
import os
import chardet
import re
import operator
from collections import Counter
import nltk
from nltk.corpus import stopwords


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext


def clean_slash(raw_text):
    cleanr = re.compile('/.*?/')
    cleantext = re.sub(cleanr, ' ', raw_text)
    return cleantext


def clean_punctuation(raw_text):
    cleanr = re.compile('[\r\n{}()%:,."\'_-]')
    cleantext1 = re.sub(cleanr, ' ', raw_text)
    cleanr = re.compile('cdata')
    cleantext2 = re.sub(cleanr, '', cleantext1)
    cleanr = re.compile(r'\\r\\n')
    cleantext3 = re.sub(cleanr, '', cleantext2)
    cleanr = re.compile(r'\\n\\n')
    cleantext4 = re.sub(cleanr, '', cleantext3)
    return cleantext4


def clean_text(sentence):
    return clean_punctuation(clean_slash(clean_html(sentence)))


def clean_spets(word):
    spets_sym = '/\“”»«€'
    return "".join([c for c in word if c not in spets_sym])


def check_encoding(fname):
    rawdata = open(fname, "rb").read()
    result = chardet.detect(rawdata)
    return result['encoding']

def get_all_words(raw_text, min_length=3):
    mytext = clean_text(raw_text)
    return [clean_spets(w.lower()) for w in mytext.split() if len(w) > min_length and not w.isnumeric()]


def main():
    dir_name = ".\PY1_Lesson_2.3"
    json_files = list()
    xml_files = list()

    russian_stemmer = nltk.stem.snowball.RussianStemmer(ignore_stopwords=True)
    my_stop_words = set(stopwords.words('russian')+['такж', 'эт', 'котор', 'год', 'нов'])

    for file in os.listdir(dir_name):
        file_name = os.path.join(dir_name, file)
        if file.endswith(".json"):
            json_files.append((file_name, check_encoding(file_name)))
        elif file.endswith(".xml"):
            xml_files.append((file_name, check_encoding(file_name)))

    all_json_text = list()
    for file, encod in json_files:
        with open(file, encoding=encod) as f:
            jdata = json.load(f)
            print ("загружен файл: {:>29}  кодировка: {}".format(file, encod))
            news_channel = jdata['rss']['channel']['item']
            for news in news_channel:
                words = get_all_words(str(news['description']))
                all_json_text += words

    clean_json_text = [ w for w in map(russian_stemmer.stem, all_json_text) if w not in my_stop_words ]
    all_json_words_frq = sorted(Counter(clean_json_text).items(), key=operator.itemgetter(1), reverse=True)
    print("\n10 популярных слов в загруженных json текстах:\n", *all_json_words_frq[:10], '\n\n')

    all_xml_text = list()
    for file, encod in xml_files:
        with open(file, encoding=encod) as f:
            dom = minidom.parse(file=f)
            print("загружен файл: {:>29}  кодировка: {}".format(file, encod))
            items_list = dom.getElementsByTagName('item')
            for item in items_list:
                words = get_all_words(item.getElementsByTagName('description').item(0).firstChild.nodeValue)
                all_xml_text += words

    clean_xml_text = [w for w in map(russian_stemmer.stem, all_xml_text) if w not in my_stop_words]
    all_xml_words_frq = sorted(Counter(clean_xml_text).items(), key=operator.itemgetter(1), reverse=True)
    print ("\n10 популярных слов в загруженных xml текстах:\n", *all_xml_words_frq[:10], '\n\n')

if __name__ == "__main__":
    main()