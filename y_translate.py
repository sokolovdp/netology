# coding: utf-8
import requests
import argparse
import sys
from pprint import pprint

default_hint = ['de', 'es', 'fr', 'en']

YANDEX_API_KEY = 'trnsl.1.1.20170327T202730Z.19970cf342c9dcee.d664d4ea0f261d94dbee40dfc005000988b22a4f'
URL_JSON_TRANSLATE = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
URL_JSON_DETECT = 'https://translate.yandex.net/api/v1.5/tr.json/detect'


def yandex_translate(lan='en-ru', text=''):
    get_params = dict(key=YANDEX_API_KEY, text=text, lang=lan)
    r = requests.get(URL_JSON_TRANSLATE, params=get_params)

    if r.status_code != 200:
        pprint(r)
        exit(1)
    else:
        return r.json()['text']


def yandex_detect(text='', hint=','.join(default_hint)):
    get_params = dict(key=YANDEX_API_KEY, text=text, hint=hint)
    r = requests.get(URL_JSON_DETECT, params=get_params)

    if r.status_code != 200:
        pprint(r)
        exit(2)
    else:
        return r.json()['lang']


def read_text_lines(file):  # strip '\n' and spaces, plus ignore empty lines
    return [line for line in list(map(lambda l: l.strip(), file.readlines())) if line != '']


def main(ln, file_in, file_out):
    with open(file_in, 'r') as f_in:
        text_translate = read_text_lines(f_in)

    if ln is None:  # let's detect language
        ln = yandex_detect(text=text_translate[0])

    new_text = yandex_translate(lan=ln + '-ru', text='\n'.join(text_translate))

    with open(file_out, 'w') as f_out:
        for line in new_text:
            f_out.write(line + '\n')
    print('translated text placed in {} file, original language is {}'.format(file_out, ln))
    exit()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--from", dest="file_from", action="store", required=True,
                    help="file with text to be translated to russian")
    ap.add_argument("-t", "--to", dest="file_to", action="store",
                    help="file to write translated text, default name: source_file-RUS.txt")
    ap.add_argument("-l", "--lang", dest="ln", action="store",
                    help="language code, default is 'en', available codes are: " + ",".join(default_hint))
    args = ap.parse_args(sys.argv[1:])

    if args.file_to is None:
        args.file_to = args.file_from + '-RUS.txt'
    if (args.ln is not None) and (args.ln not in default_hint):
        print("invalid language code:", args.ln, " language will be detected automatically")
        args.ln = None

    main(args.ln, args.file_from, args.file_to)
