
from random import choice


"""

Модуль, содержащий уровни игры и функции для работы с уровнями

"""


SIZE = 12

"""
    0 - обычная клетка (Grass)
    10 - выход из лабиринта
    1 - обычная стена
    11 - нерушимая стена
    2 - местоположение игрока
    3 - арсенал
    41,42,43 - телепорты
    6 - клад
    7 - бомба
    8 - госпиталь
    9 - река

    # пустой уровень
    [
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]
    ],


"""

__all_levels = [
    # 1
    [
        [11, 11, 11, 11, 11, 11, 11, 10, 11, 11, 11, 11],
        [11,  3,  0,  0,  0,  0,  1,  2,  1, 42,  0, 11],
        [11,  0,  0,  0,  0,  0,  7,  0,  1,  7, 41, 11],
        [11,  1,  1,  1,  1,  0,  0,  0,  1,  1,  1, 11],
        [11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  0,  0,  0,  1,  0,  0,  0,  7,  0, 10],
        [11,  0,  1,  1,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  2, 41,  1,  0,  0,  9,  1,  1,  1,  1, 11],
        [11,  1,  1,  1,  0,  0,  9,  1, 42,  2,  0, 11],
        [11,  7,  0,  0,  0,  8,  9,  1,  2,  0,  0, 11],
        [10,  0,  2,  9,  9,  9,  9,  1,  0,  0,  6, 11],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]
    ],

    # 2
    [
        [11, 10, 11, 11, 11, 11, 11, 10, 11, 11, 11, 11],
        [11,  0,  0,  0,  0, 41,  1,  0,  0, 42,  0, 11],
        [11,  0,  1,  7,  0,  0,  1,  2,  0,  7,  0, 11],
        [11,  8,  1,  0,  0,  0,  1,  0,  0,  0,  0, 11],
        [11,  1,  1,  2,  0,  9,  9,  9,  0,  0,  2, 11],
        [11,  0,  7,  0,  0,  9,  6,  1,  1,  1,  1, 11],
        [11,  0,  0,  0,  0,  9,  7,  1,  0, 42,  0, 11],
        [11,  0,  1,  9,  9,  0,  0,  1,  1,  0,  0, 11],
        [10,  0,  1,  9,  0,  0,  0,  0,  0,  0,  0, 11],
        [11,  0,  1,  9,  0,  1, 41,  0,  0,  2,  0, 11],
        [11,  3,  1,  9,  2,  1,  0,  0,  0,  0,  0, 11],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]
    ],

    # 3
    [
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
        [11,  0, 41,  9, 41,  1,  0,  0,  0,  0,  2, 11],
        [11,  0,  7,  9,  0,  1,  0,  1,  0,  8,  0, 11],
        [11,  6,  1,  9,  0,  0,  0,  1,  0,  0,  0, 11],
        [11,  1,  1,  9,  1,  1,  7,  1,  2,  0,  1, 11],
        [11,  9,  9,  9,  0,  0,  0,  0,  0,  0,  0, 10],
        [11,  9, 42,  0,  0,  1,  0,  1, 42,  0,  1, 11],
        [11,  9,  0,  1,  2,  0,  2,  0,  0,  0,  0, 11],
        [11,  9,  0,  0,  0,  0,  0,  0,  1,  0,  0, 11],
        [11,  0,  0,  1,  7,  1,  0,  1,  1,  1,  0, 11],
        [11,  2,  0,  1,  7,  1,  0,  0,  7,  1,  3, 11],
        [11, 11, 11, 11, 11, 11, 11, 11, 10, 11, 11, 11]
    ],

    # 4
    [
        [11, 11, 11, 11, 10, 11, 11, 11, 11, 11, 11, 11],
        [11, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 11],
        [11, 0, 7, 0, 0, 0, 0, 2, 0, 1, 0, 11],
        [11, 0, 0, 0, 7, 0, 1, 1, 0, 7, 0, 11],
        [11, 2, 0, 0, 0, 0, 41, 1, 0, 0, 2, 11],
        [11, 1, 0, 0, 9, 9, 9, 9, 9, 9, 9, 11],
        [11, 8, 0, 0, 9, 0, 0, 0, 0, 0, 0, 11],
        [11, 1, 0, 0, 9, 0, 1, 1, 1, 1, 0, 11],
        [11, 0, 0, 0, 9, 0, 1, 6, 41, 1, 0, 11],
        [11, 0, 7, 0, 9, 0, 1, 1, 1, 1, 0, 11],
        [11, 2, 0, 0, 9, 0, 1, 0, 7, 0, 2, 11],
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 11, 11]
    ],

    # 5
    [
        [11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 11, 11],
        [11, 6, 0, 0, 9, 1, 41, 1, 0, 0, 2, 11],
        [11, 1, 1, 0, 9, 2, 0, 1, 0, 0, 0, 11],
        [11, 42, 0, 0, 9, 0, 0, 0, 0, 7, 0, 11],
        [11, 1, 9, 9, 9, 0, 0, 0, 0, 1, 0, 11],
        [11, 9, 9, 7, 0, 0, 0, 0, 2, 1, 8, 11],
        [11, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 11],
        [11, 0, 7, 0, 0, 9, 9, 0, 0, 0, 41, 11],
        [11, 0, 2, 0, 9, 9, 0, 0, 2, 0, 1, 11],
        [11, 0, 0, 9, 9, 0, 0, 0, 7, 0, 0, 11],
        [11, 3, 9, 9, 42, 0, 1, 0, 0, 0, 7, 11],
        [11, 11, 11, 11, 11, 11, 11, 11, 10, 11, 11, 11]
    ]

]


def get_number_of_levels():
    return len(__all_levels)


def get_random_level():
    return choice(__all_levels)


def get_numbered_level(index):
    try:
        level = __all_levels[index]
    except IndexError:
        level = __all_levels[0]
        print("No such level! Returning first one")

    return level

if __name__ == "__main__":
    print("Levels container module")
