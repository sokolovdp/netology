import json
import xml
from xml.dom import minidom
import os
import chardet
import re
import operator
from collections import Counter

dir_name = ".\PY1_Lesson_2.3"
min_length = 3
json_files = list()
xml_files = list()

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

def get_all_words(raw_text):
    mytext = clean_text(raw_text)
    return [clean_spets(w.lower()) for w in mytext.split() if len(w) > min_length and not w.isnumeric()]

def main():
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
            print ("file: {} loaded, encoding: {}".format(file, encod))
            news_channel = jdata['rss']['channel']['item']
            for news in news_channel:
                words = get_all_words(str(news['description']))
                all_json_text += words
    all_json_words_frq = sorted(Counter(all_json_text).items(), key=operator.itemgetter(1), reverse=True)
    print (all_json_words_frq[:10])

    all_xml_text = list()
    for file, encod in xml_files:
        with open(file, encoding=encod) as f:
            dom = minidom.parse(file=f)
            print("file: {} loaded, encoding: {}".format(file, encod))
            items_list = dom.getElementsByTagName('item')
            for item in items_list:
                words = get_all_words(item.getElementsByTagName('description').item(0).firstChild.nodeValue)
                all_xml_text += words
    all_xml_words_frq = sorted(Counter(all_xml_text).items(), key=operator.itemgetter(1), reverse=True)
    print (all_xml_words_frq[:10])

if __name__ == "__main__":
    main()