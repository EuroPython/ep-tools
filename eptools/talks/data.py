# coding: utf-8
"""
Functions to read talks data.
"""
from ..server_utils import epcon_fetch_file


def fetch_talk_json(out_filepath, conf='ep2016'):
    """ Create json file with talks data. """
    return epcon_fetch_file(cmd='accepted_talks_abstracts {}'.format(conf),
                            fpath=out_filepath)

