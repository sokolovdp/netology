import argparse
import sys

default_dir = '.'
default_size = 200


def main(dir_n, size_):
    print(dir_n, size_ / 100)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", dest="dir", action="store", default=default_dir,
                    help="path to directory with images")
    ap.add_argument("-s", "--size", dest="size", action="store", type=int, default=default_size,
                    help="new image width in pixels")
    args = ap.parse_args(sys.argv[1:])

    main(args.dir, args.size)
