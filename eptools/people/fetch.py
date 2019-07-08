
"""
Functions to get the data of conference participants.
"""
import requests

from eptools.server_utils import epcon_fetch_file


def fetch_participant_csv(out_filepath, conference):
    """ Create csv file with participants with an assigned ticket. """
    return epcon_fetch_file(cmd="get_attendees_csv {} {}".format(conference, "complete"), fpath=out_filepath)


def fetch_users(out_filepath):
    """ Create a json file with the users in the database."""
    return epcon_fetch_file(cmd="users", fpath=out_filepath)


def fetch_ticketless_csv(out_filepath, conference):
    """ Create csv file with participants without ticket.  """
    return epcon_fetch_file(cmd="get_attendees_csv {} {}".format(conf, "incomplete"), fpath=out_filepath)


def fetch_ticket_profiles(out_filepath, conference, status="all", nondups=False, raise_=False, ticket_id=""):
    """ Create a json file with the all the tickets of the conference.
        make_option('--status',
                    choices=['all', 'complete', 'incomplete'],
                    help='Status of the orders related with the tickets.',
        make_option('--nondups',
                    help='If enables will remove the tickets with '
                         'same owner/email.',
        make_option('--raise',
                    help='If enabled will raise any error that it may find.',
        make_option('--ticket-id',
                    help='Will output the profile of the given ticket only.',
    """
    cmd = "ticket_profiles {} --status {}".format(conference, status)
    if nondups:
        cmd += " --nondups"

    if raise_:
        cmd += " --raise"

    if ticket_id:
        cmd += " --ticket_id {}".format(ticket_id)

    return epcon_fetch_file(cmd=cmd, fpath=out_filepath)


def genderize(first_name):
    """ Use genderize.io to return a dictionary with the result of the
    probability of a first name being of a man or a woman.
    Example: {'count': 5856,
              'gender': 'male',
              'name': 'Alex',
              'probability': '0.87'}

    Parameters
    ----------
    first_name: str

    Returns
    -------
    query_result: dict
    """
    return requests.get(
        "https://api.genderize.io/",
        params={"name": first_name}
    ).json()
