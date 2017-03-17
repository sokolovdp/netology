# Программа (мульти-процессорная версия) изменяет размер всех картинок в указанной директории
#  - вызов: resize.py [-d <directory/subdirectory>] [-s <new_size>]
#  - если директория не указана, то поиск осуществляется в текущей директории
#  - конвертируются все файлы  с расширениями 'jpg', 'png', 'jpeg', 'gif', 'bmp'
#  - для Windows: если имя директории содержит пробелы, то имя указывается в кавычках: "Advanced Migrations"
#  - директория ищется относительно текущей директории
#  - конвертируемые файлы помещаются в директорию в resized_images


import sys
import os
from getopt import GetoptError, getopt
import shutil
import subprocess
from multiprocessing import Process


help_line = 'usage: resize.py [-d <directory/subdirectory>] [-s <new_size>] '
default_size = 100
image_file_ext = ('jpg', 'png', 'jpeg', 'gif', 'bmp')
result_dir = 'resized_images'
max_processes = 4


def get_dir_size(argv):
    try:
        opts, args = getopt(argv, "hd:s:", ["dir=", "size="])
    except GetoptError:
        print(help_line)
        sys.exit(1)
    dir_n = ''
    pic_size = default_size
    for opt, arg in opts:
        if opt == '-h':
            print(help_line)
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir_n = arg
        elif opt in ("-s", "--size"):
            try:
                pic_size = int(arg)
            except ValueError:
                print(help_line)
                sys.exit(2)
    return dir_n, pic_size


def find_working_dir(dir_n):
    w_path = os.path.join(os.getcwd(), dir_n)
    if not os.path.exists(w_path):
        print('no such directory: ', w_path)
        sys.exit(3)

    return w_path


def convert_process(new_dir, files, size):
    # print('started process id:', os.getpid())
    for file in files:
        err = subprocess.call('convert.exe ' + file + ' -resize ' + str(size) + ' resized_' + file)
        if err:
            print("unexpected error: {} during image {} processing, image ignored".format(err, file))
        else:
            shutil.move('resized_' + file, new_dir)


def convert_image_files(directory, files, size):
    os.chdir(directory)
    print('\n{0} images in folder: {1} will be resized'.format(len(files), directory.split('\\')[-1], size))

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    else:
        shutil.rmtree(result_dir)
        os.makedirs(result_dir)

    splitted_list = [files[i:i+max_processes] for i in range(0, len(files), max_processes)]
    for short_list in splitted_list:
        p = Process(target=convert_process, args=(result_dir, short_list, size,))
        p.start()
        p.join()


def main(argv):
    dir_name, resize = get_dir_size(argv)
    working_path = find_working_dir(dir_name)

    image_files = list()
    for file in os.listdir(working_path):
        if file.endswith(image_file_ext):
            image_files.append(file)
    if len(image_files) == 0:
        print('no image files in the directory: "' + working_path + '"')
        sys.exit()

    convert_image_files(working_path, image_files, resize)


if __name__ == "__main__":
    main(sys.argv[1:])
