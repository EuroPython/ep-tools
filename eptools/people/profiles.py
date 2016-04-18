# coding: utf-8

"""
This is a intro on how to fill the PeopleRegistry with contact details of
all the conference participants and their roles.
This will be mostly to be able to produce the conference badges correctly and send emails.
"""

import io
import json
from itertools import chain

from ..people import (  ParticipantsRegistry,
                        fetch_ticket_profiles,
                        contact_regex2,
                        parse_contact,
                        )

from ..talks import (fetch_talks_json,
                     get_type_speakers,
                    )


# these files can be generated/downloaded from the server
talks_json     = 'talks_with_votes.json'
profiles_json  = 'profiles.json'

# these files were created manually (you need these)
organizers_txt = 'organizers.txt'
volunteers_txt = 'volunteers.txt'
epsmembers_txt = 'epsmembers.txt'


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def load_id_json(json_path, add_id=False):
    if not add_id:
        return [item for eid, item in json.load(open(json_path)).items()]
    else:
        items = []
        for eid, item in json.load(open(json_path)).items():
            item['id'] = eid
            items.append(item)
        return items


def read_lines(txt_file):
    with io.open(txt_file, 'rt', encoding='utf-8') as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def read_names(txt_file):
    lines = read_lines(txt_file)
    return [(name.split(' ')[0], ' '.join(name.split(' ')[1:])) for name in lines]


def read_contacts(txt_file=organizers_txt):
    return [parse_contact(line, regex=contact_regex2) for line in read_lines(txt_file)]


def fetch_files(conf='ep2016', host='europython.io', talk_status='accepted'):
    """
    Parameters
    ----------
    fetch_data: bool
        If True will download the data from the web server.

    conf: str
        The string identifying the conference.

    host: str
        The IP address to where the web server is.
        These parameters might not be enough to set up the connection to the server to
        download the data.

        Note:
        You may want to check the server_utils.epcon_fetch_file function:
        change the default arguments or make them available through this function.

    talk_status: str
        choices: 'proposed', 'accepted'
        In the end this should be 'accepted'
        Be careful, if the talks.json file is already downloaded with not accepted talks
        and `fetch_data` is False the result won't be correct.
        You need to either set `fetch_data` to True or download a new talks.json
        file with the accepted talks.

    Returns
    -------
    profiles_file, talks_file: str
        Files paths of the fetched data.
    """
    profiles_file = fetch_ticket_profiles(profiles_json, conf=conf)
    _             = fetch_talks_json     (talks_json,    conf=conf, status=talk_status,
                                          host=host,     with_votes=True)
    return profiles_file, talks_json


def get_profiles_registry():
    """ Return a ParticipantsRegistry with the ticket profiles data and the people's roles.

    Returns
    -------
    pr: ParticipantsRegistry
    """
    talks = {}
    people = load_id_json(profiles_json, add_id=True)
    type_talks = dict(json.load(open(talks_json)).items())
    _ = [talks.update(talkset) for ttype, talkset in type_talks.items()]

    # speakers and trainers
    type_speakers = get_type_speakers(talks)
    organizers    = read_contacts(organizers_txt)
    volunteers    = read_contacts(volunteers_txt)
    epsmembers    = read_contacts(epsmembers_txt)

    # create and fill the registry
    pr = ParticipantsRegistry(people)

    for stype, emails in type_speakers.items():
        pr.set_emails_role(emails, stype)

    pr.set_emails_role([p[2] for p in organizers], 'organizer')
    pr.set_emails_role([p[2] for p in volunteers], 'volunteer')
    pr.set_emails_role([p[2] for p in epsmembers], 'epsmember')

    pr.set_names_role([(p[0], p[1]) for p in organizers], 'organizer')
    pr.set_names_role([(p[0], p[1]) for p in volunteers], 'volunteer')
    pr.set_names_role([(p[0], p[1]) for p in epsmembers], 'epsmember')

    return pr

