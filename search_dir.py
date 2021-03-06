# Программа проверяет тестовые файлы с нужным расширением в указанной директории на наличие поисковых слов
#  - вызов: search_dir.py [-h] [-d <directory/subdirectory>] [-e <file_extension>]
#  - если директория не указана, то поиск осуществляется в текущей директории
#  - если расширение не указано, то проверяются все файлы в директории
#  - для Windows: если имя директории содержит пробелы, то имя указывается в кавычках: "Advanced Migrations"
#  - директория ищется относительно текущей директории
#  - если введенного слова в найденных файлах нет, то слово игнорируется
#  - выход из программы происходит при вводе пустой строки
#  - по окончанию работы программа выдает список введенных слов и список файлов их содержаших

import sys
import os
import argparse
import chardet

default_ext = ''
default_dir = '.'


def find_working_dir(dir_n):
    w_path = os.path.join(os.getcwd(), dir_n)
    if not os.path.exists(w_path):
        print('no such directory: ', w_path)
        sys.exit(2)

    return w_path


def get_encoding(fname):
    return chardet.detect(open(fname, "rb").read())['encoding']


def word_in_file(file, word):
    try:
        with open(file, 'r', encoding=get_encoding(file)) as f:
            file_content = f.read()
        if not file_content:
            print("file: {} is empty".format(file))
        elif word in file_content:
            return True
    except UnicodeDecodeError:
        print("file: {} ignored, unknown encoding".format(file))
    except IOError as e:
        print("file: {} i/o error({})".format(file, e.errno))
    except:  # handle other i/o exceptions
        print("file: {} unexpected error: {}".format(file, sys.exc_info()[0]))

    return False


def search_in_files(directory, files):
    os.chdir(directory)
    word_list = list()
    print('\n{} files found'.format(len(files)))
    while True:
        word = input("\nword or <enter> to exit: ")
        if word == '':
            print("stopped")
            break
        temp_list = [file for file in files if word_in_file(file, word)]
        if len(temp_list):  # if word was not found ignore it
            word_list.append(word)
            files = temp_list
        print('{} files found:'.format(len(files)))
        print(*files, sep='\n')
    return files, word_list


def print_result(result):
    search_files, search_words = result
    print("\nsearch words were:")
    for word in search_words:
        print("  " + word)
    print("\nfound files are:")
    for file in search_files:
        print("  " + file)


def main(dir_name, file_ext):

    working_path = find_working_dir(dir_name)

    search_files = list()
    for file in os.listdir(working_path):
        if file.endswith(file_ext):
            search_files.append(file)
    if len(search_files) == 0:
        print('no files with extension: "' + file_ext + '" in the directory: "' + working_path + '"')
        sys.exit()

    print_result(search_in_files(working_path, search_files))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", dest="dir", action="store", default=default_dir,
                    help="path to directory with files to be checked")
    ap.add_argument("-e", "--ext", dest="ext", action="store", default=default_ext,
                    help="files extension to search in")
    args = ap.parse_args(sys.argv[1:])

    main(args.dir, args.ext)
