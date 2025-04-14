import copy
import logging
import logging.config
import json


def setup_logging() -> None:
    with open('logging_config.json', 'r') as f:
        config = json.load(f)
    logging.config.dictConfig(config)


def get_colors_simple() -> list[tuple[int, ...]]:
    r = list()
    for c in range(3):
        i = c
        j = (i + 1) % 3
        for v in range(256):
            t = [0, 0, 0]
            t[i] = 255 - v
            t[j] = v
            r.append(tuple(t))
    return r


def bend_list(minimum: int, maximum: int, length: int) -> list[int]:
    if length < 1:
        return list()
    maximum = max(minimum, maximum)
    range_length = maximum - minimum
    ratio = range_length / length
    base = range(length)
    return list(map(lambda n: int(n * ratio) + minimum, base))


def shrink_list(lst: list, new_length: int) -> list:
    old_length = len(lst)
    if old_length <= new_length:
        return copy.deepcopy(lst)
    result_lst = list()
    length_ratio = int(old_length / new_length)
    for i in range(0, old_length, length_ratio):
        result_lst.append(lst[i])
    return result_lst
