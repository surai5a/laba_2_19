#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json
import jsonschema
from jsonschema import validate
import pathlib

path = pathlib.Path('C:/Users/Vadym/data.txt')


schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
        "shop" : {"type" : "string"}
    },
}


def add_goods(goods, args):
    # Создать словарь.
    good = {
        'name': args.name,
        'shop': args.shop,
        'price': args.price,
    }
    # Добавить словарь в список.
    goods.append(good)
    # Отсортировать список в случае необходимости.
    if len(goods) > 1:
        goods.sort(key=lambda item: item.get('name', ''))


def display_goods(goods):
    """
    Отобразить список товаров.
    """
    # Проверить, что список товаров не пуст.
    if goods:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "№",
                "Название",
                "Магазин",
                "Цена"
            )
        )
        print(line)
        # Вывести данные о всех товарах.
        for idx, good in enumerate(goods, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    good.get('name', ''),
                    good.get('shop', ''),
                    good.get('price', 0)
                )
            )
        print(line)

    else:
        print("Список товаров пуст.")


def select_goods(goods, shop):
    """
    Выбрать товары магазина.
    """

    # Счетчик записей.
    count = 0

    # Сформировать список товаров.
    result = []

    for good in goods:
        if shop == good.get('shop', shop):
            count += 1
            result.append(good)

    # Проверка на отсутствие товаров или выбранного магазина.
    if count == 0:
        print("Такого магазина не существует либо нет товаров.")
    else:
        # Возвратить список выбранных товаров.
        return result


def save_goods(file_name, goods):
    """
    Сохранить все магазины в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(goods, fout, ensure_ascii=False, indent=4)


def load_goods(file_name):
    """
    Загрузить все магазины из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        f = json.load(fin)
    err_count = 0
    print("...валидация...")
    for idx, item in enumerate(f):
        try:
            validate(item, schema)
            sys.stdout.write("Запись {}: OK\n".format(idx))
        except jsonschema.exceptions.ValidationError as ve:
            sys.stderr.write("Запись {}: ОШИБКА\n".format(idx))
            sys.stderr.write(str(ve) + "\n")
            err_count += 1
    if err_count > 0:
        print("JSON-файл не прошел валидацию.\nФайл не будет загружен.")
    else:
        print(f"JSON-файл успешно загружен\nФайл = {file_name}")
        return f


def main():
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        required=False,
        action="store",
        help="The data file name"
    )
    file_parser.add_argument(
        "-D",
        "--default",
        required=False,
        action="store_true",
        help="Checkbox for default folder"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("goods")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления товара.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new good"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The good's name"
    )
    add.add_argument(
        "-s",
        "--shop",
        action="store",
        help="The good's shop"
    )
    add.add_argument(
        "-p",
        "--price",
        action="store",
        type=int,
        required=True,
        help="Price of the good"
    )

    # Создать субпарсер для отображения всех товаров.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all goods"
    )

    # Создать субпарсер для выбора товаров.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the goods"
    )

    select.add_argument(
        "-S",
        "--shop_select",
        action="store",
        required=True,
        help="The required shop"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args()

    # Получить имя файла.
    data_file = args.data
    if not data_file:
        if args.default:
            data_file = path
        if not data_file:
            data_file = os.environ.get("WORKERS_DATA")
            if not data_file:
                print("The data file name is absent", file=sys.stderr)
                sys.exit(1)

    # Загрузить все товары из файла, если файл существует.
    is_dirty = False
    if os.path.exists(data_file):
        goods = load_goods(data_file)
    else:
        goods = []

    # Добавить работника.
    if args.command == "add":
        add_goods(goods, args)
        is_dirty = True

    # Отобразить всех работников.
    elif args.command == "display":
        display_goods(goods)

    # Выбрать требуемых работников.
    elif args.command == "select":
        selected = select_goods(goods, args.shop_select)
        display_goods(selected)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_goods(data_file, goods)


if __name__ == '__main__':
    main()
