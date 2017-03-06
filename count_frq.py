import json
from xml.dom import minidom
import os
import chardet
import re
import operator
from collections import Counter
import nltk
from nltk.corpus import stopwords

russian_stemmer = nltk.stem.snowball.RussianStemmer(ignore_stopwords=True)
my_stop_words = set(stopwords.words('russian') + ['такж', 'эт', 'котор', 'год', 'нов', 'дан', 'гост'])
dir_name = "PY1_Lesson_2.3"
max_words = 10
min_word_length = 6


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
    raw_data = open(fname, "rb").read()
    result = chardet.detect(raw_data)
    return result['encoding']


def get_all_words(raw_text, min_length=min_word_length):
    mytext = clean_text(raw_text)
    return [clean_spets(w.lower()) for w in mytext.split() if len(w) > min_length and not w.isnumeric()]


def get_popular_words(n_words, words):
    stemmed_words = [w for w in map(russian_stemmer.stem, words) if w not in my_stop_words]
    popular_words = sorted(Counter(stemmed_words).items(), key=operator.itemgetter(1), reverse=True)
    return popular_words[:n_words]


def main():
    json_files = list()
    xml_files = list()

    print("{1} популярных слов длиннее {2} символов в json и xml файлах в директории {0}\n".format(dir_name, max_words,
            min_word_length))

    for file in os.listdir(dir_name):
        file_name = os.path.join(dir_name, file)
        if file.endswith(".json"):
            json_files.append((file_name, check_encoding(file_name)))
        elif file.endswith(".xml"):
            xml_files.append((file_name, check_encoding(file_name)))

    # all_json_text = list()
    for file, encod in json_files:
        with open(file, encoding=encod) as f:
            words = list()
            jdata = json.load(f)
            print("\nзагружен файл: {}  кодировка: {}".format(file, encod))
            news_channel = jdata['rss']['channel']['item']
            for news in news_channel:
                words += get_all_words(str(news['description']))
                # all_json_text += words
            print(max_words, "популярных слов в загруженном тексте:\n",
                *get_popular_words(max_words, words))   # all_json_text))

    # all_xml_text = list()
    for file, encod in xml_files:
        with open(file, encoding=encod) as f:
            words = list()
            dom = minidom.parse(file=f)
            print("\nзагружен файл: {}  кодировка: {}".format(file, encod))
            items_list = dom.getElementsByTagName('item')
            for item in items_list:
                words += get_all_words(item.getElementsByTagName('description').item(0).firstChild.nodeValue)
                # all_xml_text += words
            print(max_words, "популярных слов в загруженном тексте:\n",
                    *get_popular_words(max_words, words))   # all_xml_text))

if __name__ == "__main__":

    main()
