# coding: utf-8
"""
Functions to read talks data.
"""
import tempfile
import json

from invoke import task

from ..server_utils import epcon_fetch_file


def _call_for_talks(out_filepath, status='accepted', conf='ep2016', host='europython.io'):
    """ Create json file with talks data. `status` choices: ['accepted', 'proposed']
    """
    return epcon_fetch_file(cmd='talk_abstracts {} --talk_status {}'.format(conf, status),
                            fpath=out_filepath,
                            host=host)


def load_events(talks_filepath):
    """ Return a list of event records from the talks file."""
    sessions = json.load(open(talks_filepath, 'r'))
    events   = [event for name in sessions for event in sessions[name].values()]

    return events


@task
def fetch_talks_json(out_filepath='', status='proposed', conf='ep2016', host='europython.io'):
    """ Return the talks in a json format. `status` choices: ['accepted', 'proposed']
    """
    if not out_filepath:
        out_filepath = tempfile.NamedTemporaryFile(suffix='.json').name

    _ = _call_for_talks(out_filepath=out_filepath, status=status, conf=conf, host=host)

    with open(out_filepath, 'r') as f:
        talks = json.load(f)

    return talks
