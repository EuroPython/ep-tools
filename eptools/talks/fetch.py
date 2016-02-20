# coding: utf-8
"""
Functions to read talks data.
"""
import json

from ..server_utils import epcon_fetch_file


def fetch_talk_json(out_filepath, conf='ep2016'):
    """ Create json file with talks data. """
    return epcon_fetch_file(cmd='accepted_talks_abstracts {}'.format(conf),
                            fpath=out_filepath)


def load_events(talks_filepath):
    """ Return a list of event records from the talks file."""
    sessions = json.load(open(talks_filepath, 'r'))
    events   = [event for name in sessions for event in sessions[name].values()]

    return events
