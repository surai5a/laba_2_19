#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pathlib
import os

tree_str = ''
CURRENT_PATH = os.getcwd()


def generate_tree(pathname, n=0):
    global tree_str
    if pathname.is_file():
        tree_str += '    |' * n + '-' * 4 + pathname.name + '\n'
    elif pathname.is_dir():
        tree_str += '    |' * n + '-' * 4 + \
            str(pathname.relative_to(pathname.parent)) + '\\' + '\n'
        for cp in pathname.iterdir():
            generate_tree(cp, n + 1)


def generate_tree_dirs(pathname, n=0):
    global tree_str
    if pathname.is_dir():
        tree_str += '    |' * n + '-' * 4 + \
            str(pathname.relative_to(pathname.parent)) + '\\' + '\n'
        for cp in pathname.iterdir():
            generate_tree_dirs(cp, n + 1)


def save_output(file_name):
    with open(file_name, "w", encoding="utf-8") as fout:
        fout.write(tree_str)


def main():
    file = argparse.ArgumentParser(add_help=True)
    file.add_argument(
        "path",
        action='store',
        nargs='?',
        default=CURRENT_PATH,
        help='Store the directory path'
    )
    file.add_argument(
        '-d',
        "--dirs",
        action="store_true",
        required=False,
        help="Enable dirs only mode"
    )
    file.add_argument(
        '-s',
        '--save',
        action='store',
        required=False,
        help='Saves the output tree'
    )

    args = file.parse_args()

    directory = pathlib.Path(args.path)
    print(directory)
    if args.dirs:
        generate_tree_dirs(directory)
    else:
        generate_tree(directory)

    print(args.save)
    if args.save:
        save_output(args.save)
    else:
        print(tree_str)


if __name__ == '__main__':
    main()
