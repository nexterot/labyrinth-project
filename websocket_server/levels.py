from random import choice

SIZE = 12

__all_levels = [
    # 1
    [
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 3, 0, 0, 0, 0, 1, 0, 1, 42, 0, 1],
        [1, 0, 0, 0, 0, 0, 7, 0, 1, 7, 41, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 5, 0, 1, 0, 2, 0, 7, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 41, 1, 0, 0, 9, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 9, 1, 42, 0, 0, 1],
        [1, 7, 0, 0, 0, 8, 9, 1, 0, 0, 0, 1],
        [0, 0, 0, 9, 9, 9, 9, 1, 0, 0, 6, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
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