# coding: utf-8
"""
Utility functions for badges.
"""
import textwrap

def split_in_two(string, max_length=30):
    """ Split `string` in two strings of maximum length `max_length`.
    The rest is thrown away, sorry.
    This function looks for a `separator` before `max_length`,
    if it is found, it splits the string by the position
    of the `separator` instead of `max_length`.

    Return
    ------
    split: 2-tuple of str
    """
    wrap = textwrap.wrap(string, width=max_length)

    if len(wrap) >= 2:
        return wrap[0], wrap[1]

    return wrap[0], ''
