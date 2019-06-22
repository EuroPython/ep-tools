

"""
This is a intro on how to fill the PeopleRegistry with contact details of
all the conference participants and their roles.
This will be mostly to be able to produce the conference badges correctly
and send emails.
"""

import io
import json

from eptools.people.contact import contact_regex2, parse_contact


def load_id_json(json_path, add_id=False, id_field_name='id'):
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
        item[id_field_name] = eid
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
