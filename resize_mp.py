# Программа (мульти-процессорная версия) изменяет размер всех картинок в указанной директории
#  - вызов: resize.py [-h] [-d <directory_path>] [-s <width>]
#  - если директория не указана, то поиск осуществляется в текущей директории
#  - конвертируются все файлы  с расширениями 'jpg', 'png', 'jpeg', 'gif', 'bmp'
#  - для Windows: если имя директории содержит пробелы, то имя указывается в кавычках: "Advanced Migrations"
#  - директория ищется относительно текущей директории
#  - конвертируемые файлы помещаются в создаваемую директорию в Result

import sys
import os
import shutil
import subprocess
from multiprocessing import Process
import argparse

default_size = 100
default_dir = '.'
image_file_ext = ('jpg', 'png', 'jpeg', 'gif', 'bmp')
result_dir = 'Result'
max_processes = 4
max_images = 8


def find_working_dir(dir_n):
    w_path = os.path.join(os.getcwd(), dir_n)
    if not os.path.exists(w_path):
        print('no such directory: ', w_path)
        sys.exit(1)

    return w_path


def convert_process(new_dir, files, size):
    # print('started process id:', os.getpid())
    for file in files:
        err = subprocess.call(['convert.exe', file, '-resize', str(size), os.path.join(new_dir, 'resized_%s' % file)])
        if err:
            print("unexpected error: {} during image {} processing, file ignored".format(err, file))


def convert_image_files(directory, files, size):
    os.chdir(directory)
    print('\n{0} images in folder: {1} will be resized to {2} width'.format(len(files),
                                                                            directory.split('\\')[-1], size))

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    else:
        shutil.rmtree(result_dir)
        os.makedirs(result_dir)

    if len(files) > max_images:  # too many images let's use multiprocessing
        splitted_list = [files[i:i + max_processes] for i in range(0, len(files), max_processes)]
        for short_list in splitted_list:
            p = Process(target=convert_process, args=(result_dir, short_list, size,))
            p.start()
            p.join()
    else:  # few images, so we can handle them in one process
        convert_process(result_dir, files, size)


def main(dir_name, resize):
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
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", dest="dir", action="store", default=default_dir,
                    help="path to directory with images")
    ap.add_argument("-s", "--size", dest="size", action="store", type=int, default=default_size,
                    help="new image width in pixels")
    args = ap.parse_args(sys.argv[1:])

    main(args.dir, args.size)
