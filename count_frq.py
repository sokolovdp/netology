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
my_stop_words = set(stopwords.words('russian') + ['котор', 'прошл', 'сообща', 'сообщ', 'турист'])
dir_name = "PY1_Lesson_2.3"
max_words = 10
min_word_length = 6


def clean_html(raw_html):
    return re.sub('<.*?>', ' ', raw_html)


def clean_slash(raw_text):
    return re.sub('/.*?/', ' ', raw_text)


def clean_punctuation(raw_text):
    cleantext = re.sub('[\r\n{}…()!&#;%:,."\'’‘_\-/\\“”»«€–0123456789]', ' ', raw_text)
    return re.sub('\\\\r|\\\\n', '', re.sub('cdata|\\n', ' ', cleantext))


def clean_text(raw_text):
    return clean_punctuation(clean_slash(clean_html(raw_text)))


def check_encoding(fname):
    raw_data = open(fname, "rb").read()
    result = chardet.detect(raw_data)
    return result['encoding']


def get_all_words(raw_text, min_length=min_word_length):
    mytext = clean_text(raw_text)
    return [w.lower() for w in mytext.split() if len(w) > min_length] # and not w.isnumeric()]


def get_popular_words(n_words, words):
    stemmed_words = [w for w in map(russian_stemmer.stem, words) if w not in my_stop_words]
    popular_words = sorted(Counter(stemmed_words).items(), key=operator.itemgetter(1), reverse=True)
    return popular_words[:n_words]


def main():
    print("{1} популярных слов длиннее {2} символов в json и xml файлах, директория: {0}\n".format(dir_name, max_words,
            min_word_length))

    json_files = list()
    xml_files = list()
    for file in os.listdir(dir_name):
        file_name = os.path.join(dir_name, file)
        if file.endswith(".json"):
            json_files.append((file_name, check_encoding(file_name)))
        elif file.endswith(".xml"):
            xml_files.append((file_name, check_encoding(file_name)))

    for file, encod in json_files:
        with open(file, encoding=encod) as f:
            words = list()
            jdata = json.load(f)
            print("\nфайл: {}  кодировка: {}".format(file, encod))
            news_channel = jdata['rss']['channel']['item']
            for news in news_channel:
                words += get_all_words(str(news['description']))
            # print(*words)
            # input('continue?')
            print(max_words, "популярных слов в загруженном тексте:\n",
                *get_popular_words(max_words, words))

    for file, encod in xml_files:
        with open(file, encoding=encod) as f:
            words = list()
            dom = minidom.parse(file=f)
            print("\nфайл: {}  кодировка: {}".format(file, encod))
            items_list = dom.getElementsByTagName('item')
            for item in items_list:
                words += get_all_words(item.getElementsByTagName('description').item(0).firstChild.nodeValue)
            print(max_words, "популярных слов в загруженном тексте:\n",
                    *get_popular_words(max_words, words))

if __name__ == "__main__":
    main()
