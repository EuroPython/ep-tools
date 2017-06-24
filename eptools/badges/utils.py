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
    string = string.strip()
    if not string:
        return '', ''

    wrap = textwrap.wrap(string, width=max_length)
    if len(wrap) >= 2:
        return wrap[0], wrap[1]

    return wrap[0], ''


def is_subsequence(string1, string2, m=None, n=None, case_sensitive=False):
    """ Returns true if str1 is a subsequence of str2.
    m is length of str1 and n is length of str2
    """
    if m is None:
        m = len(string1)

    if n is None:
        n = len(string2)

    if not case_sensitive:
        string1 = string1.lower()
        string2 = string2.lower()

    # Base Cases
    if m == 0:    return True
    if n == 0:    return False

    # If last characters of two strings are matching
    if string1[m-1] == string2[n-1]:
        return is_subsequence(string1, string2, m-1, n-1, case_sensitive=True)

    # If last characters are not matching
    return is_subsequence(string1, string2, m, n-1, case_sensitive=True)
