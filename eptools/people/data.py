# coding: utf-8
"""
Functions to get the data of conference participants.
"""
from ..server_utils import epcon_fetch_file


def fetch_participant_csv(out_filepath, conf='ep2016'):
    """ Create csv file with participants with an assigned ticket. """
    return epcon_fetch_file(cmd='get_attendees_csv {} {}'.format(conf, 'complete'),
                            fpath=out_filepath)


def fetch_ticketless_csv(out_filepath, conf='ep2016'):
    """ Create csv file with participants without ticket.  """
    return epcon_fetch_file(cmd='get_attendees_csv {} {}'.format(conf, 'incomplete'),
                            fpath=out_filepath)
