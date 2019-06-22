
"""
Functions to read talks data.
"""
import tempfile
import json

from ..server_utils import epcon_fetch_file


def _call_for_talks(out_filepath, status="accepted", conference="ep2017", host="europython.io", with_votes=False):
    """ Create json file with talks data. `status` choices: ['accepted', 'proposed']
    """
    cmd = "talk_abstracts {} --talk_status {}".format(conference, status)

    if with_votes:
        cmd += " --votes"

    return epcon_fetch_file(cmd=cmd, fpath=out_filepath, host=host)


def load_events(talks_filepath):
    """ Return a list of event records from the talks file."""
    sessions = json.load(open(talks_filepath, "r"))
    events = [event for name in sessions for event in sessions[name].values()]

    return events


def fetch_talks_json(out_filepath="", status="proposed", conference="ep2017", host="europython.io", with_votes=False):
    """ Return the talks in a json format. `status` choices: ['accepted', 'proposed']
    """
    if not out_filepath:
        out_filepath = tempfile.NamedTemporaryFile(suffix=".json").name

    _call_for_talks(out_filepath=out_filepath, status=status, conference=conference, host=host, with_votes=with_votes)

    with open(out_filepath, "r") as f:
        talks = json.load(f)

    return talks
