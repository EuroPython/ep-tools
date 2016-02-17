# coding: utf-8
"""
Utility functions for badges.
"""


def split_in_two(string, separator=' ', max_length=30):
    """ Split `string` in two strings of maximum length `max_length`.
    The rest is thrown away, sorry.
    This function looks for a `separator` before `max_length`,
    if it is found, it splits the string by the position
    of the `separator` instead of `max_length`.

    Return
    ------
    split: 2-tuple of str
    """
    if len(string) <= max_length:
        return string, ''

    idx = string[:max_length].rfind(separator)
    if idx > 0:
        return string[:idx], string[idx+1:idx+1+max_length]
    else:
        return string[:max_length], string[max_length:max_length*2]
