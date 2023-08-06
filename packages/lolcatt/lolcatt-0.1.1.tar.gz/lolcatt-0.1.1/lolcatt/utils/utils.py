#!/usr/bin/env python3


def marquee(s: str, max_len: int, step_size: int) -> str:
    """
    Yields a string that is max_len characters long, and shifts the string
    by step_size each time.

    :param s: The string to be shifted
    :param max_len: The maximum length of the string
    :param step_size: The number of characters to shift the string by
    :return: A string that is max_len characters long and appropriately shifted
    """
    while True:
        if len(s) < max_len:
            yield s
        else:
            s = f'{s[step_size:]}{s[:step_size]}'
            yield s[:max_len]
