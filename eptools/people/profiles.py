

"""
This is a intro on how to fill the PeopleRegistry with contact details of
all the conference participants and their roles.
This will be mostly to be able to produce the conference badges correctly
and send emails.
"""

import io
import json
from itertools import chain

from ..people import (
    ParticipantsRegistry,
    fetch_ticket_profiles,
    contact_regex2,
    parse_contact,
)

from ..talks import fetch_talks_json, get_type_speakers

from .data import clean_name

# these files can be generated/downloaded from the server
talks_json = "accepted_talks.json"
profiles_json = "profiles.json"

# these files were created manually (you need these)
peoplelist_files = {
    "organizer": "organizers.txt",
    "volunteer": "volunteers.txt",
    "epsmember": "epsmembers.txt",
    "keynote": "keynoters.txt",
}


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def load_id_json(json_path, add_id=False):
    """ Return a list of the objects in the json file.
    If the JSON is a dictionary, will insert the object key value
    into the object's 'id' field.
    """
    if not add_id:
        return [item for eid, item in json.load(open(json_path)).items()]

    data = json.load(open(json_path))
    if isinstance(data, list):
        return data

    items = []
    for eid, item in data.items():
        item["id"] = eid
        items.append(item)
    return items


def read_lines(txt_file):
    with io.open(txt_file, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def read_names(txt_file):
    lines = read_lines(txt_file)
    return [(name.split(" ")[0], " ".join(name.split(" ")[1:])) for name in lines]


def read_contacts(txt_file):
    return [parse_contact(line, regex=contact_regex2) for line in read_lines(txt_file)]


def fetch_files(conf="ep2017", host="europython.io", talk_status="accepted"):
    """
    Parameters
    ----------
    fetch_data: bool
        If True will download the data from the web server.

    conf: str
        The string identifying the conference.

    host: str
        The IP address to where the web server is.
        These parameters might not be enough to set up the connection to the
        server to download the data.

        Note:
        You may want to check the server_utils.epcon_fetch_file function:
        change the default arguments or make them available through this
        function.

    talk_status: str
        choices: 'proposed', 'accepted'
        In the end this should be 'accepted'
        Be careful, if the talks.json file is already downloaded with not
        accepted talks and `fetch_data` is False the result won't be correct.
        You need to either set `fetch_data` to True or download a new talks.json
        file with the accepted talks.

    Returns
    -------
    profiles_file, talks_file: str
        Files paths of the fetched data.
    """
    profiles_file = fetch_ticket_profiles(profiles_json, conf=conf)
    fetch_talks_json(
        talks_json, conf=conf, status=talk_status, host=host, with_votes=True
    )
    return profiles_file, talks_json


def get_profiles_registry(profiles_json=profiles_json, talks_json=talks_json):
    """ Return a ParticipantsRegistry with the ticket profiles data and the
    people's roles.

    Returns
    -------
    pr: ParticipantsRegistry
    """
    talks = {}
    people = load_id_json(profiles_json, add_id=True)
    type_talks = dict(json.load(open(talks_json)).items())

    for ttype, talkset in type_talks.items():
        talks.update(talkset)

    # create and fill the registry
    pr = ParticipantsRegistry(people)

    type_speakers = get_type_speakers(talks)
    for stype, emails in type_speakers.items():
        pr.set_emails_role(emails, stype)

    # keynotes, organizers, volunteers....
    peopleslists = {
        ptype: read_contacts(txtfile) for ptype, txtfile in peoplelist_files.items()
    }

    for ptype, people in peopleslists.items():
        pr.set_emails_role([p[2] for p in people], ptype)
        pr.set_names_role([(clean_name(p[0]), clean_name(p[1])) for p in people], ptype)

    return pr
