# coding: utf-8
"""
Functions to read talks data.
"""
import json

from invoke import task

from ..server_utils import epcon_fetch_file


@task
def fetch_talk_json(out_filepath, status='accepted', conf='ep2016'):
    """ Create json file with talks data. `status` choices: ['accepted', 'proposed']
    """
    return epcon_fetch_file(cmd='talk_abstracts {} --talk_status {}'.format(conf, status),
                            fpath=out_filepath)


def load_events(talks_filepath):
    """ Return a list of event records from the talks file."""
    sessions = json.load(open(talks_filepath, 'r'))
    events   = [event for name in sessions for event in sessions[name].values()]

    return events
