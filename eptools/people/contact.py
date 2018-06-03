

import re
from copy import copy
from enum import Enum
from collections import namedtuple


# Define attendee types
ATTENDEE_TYPE = Enum("Attendee_Type", "keynote organizer trainer speaker attendee")
TALK_TYPE = Enum("Talk_Type", "talk tutorial helpdesk")

# contact class
CONTACT_FIELDS = (
    "id",
    "name",
    "surname",
    "tagline",
    "company",
    "pypower",
    "tshirt",
    "email",
    "phone",
    "title",
    "compweb",
    "persweb",
)

Contact = namedtuple("Contact", CONTACT_FIELDS)

# regexes
email_regex = r"[\w0-9\.\+\_\-]+@[\w0-9\.\+\_\-]+[\.\w+]+"
name_regex = r"[\w0-9\.\_\-\']+"
person_name = r"{name}([ ]{name})*".format(name=name_regex)

# '<name, surname> email'
contact_regex1 = r"^<(?P<name>{name})[ ]*,[ ]*((?P<surname>{name}))>" "[ ]*(?P<email>{email})?$".format(
    name=person_name, email=email_regex
)

# name, surname <email>
contact_regex2 = "^(?P<name>{name})[ ]*,[ ]*(?P<surname>{name})" "([ ]*<(?P<email>{email})>)?$".format(
    name=person_name, email=email_regex
)


def stringify(adict):
    """ Convert all values of `adict` to str."""
    for key, val in adict.items():
        if not isinstance(val, str):
            adict[key] = str(val)
    return adict


def contact_from_dict(person_info):
    """ Create a Contact object from the `person_info` dictionary."""
    person = stringify(copy(person_info))

    if "t-shirt" in person:
        person["tshirt"] = person.get("t-shirt", None)
        del person["t-shirt"]

    person["persweb"] = person["persweb"].replace("http://", "")
    person["compweb"] = person["compweb"].replace("http://", "")
    if not person["company"]:
        person["company"] = person["compweb"]

    return Contact(**person)


def parse_contact(string, regex=contact_regex2):
    """ Parse a string in the format given by the regex
    Returns
    -------
    given_name, family_name, email: str
    """
    pattern = re.compile(regex, re.IGNORECASE | re.UNICODE)
    matches = pattern.match(string)
    if matches is None:
        raise ValueError("Error reading contact in line {}.".format(string))

    m = matches.groupdict()
    return m["name"], m["surname"], m["email"]


def read_contacts_file(filepath, contact_regex=contact_regex2):
    """ Read a list of contacts from a text file in `filepath`.
    The contact format is: <FirstName, SurName> EmailAddress

    Parameters
    ----------
    filepath: str
        Path to the input file

    Returns
    -------
    email: dict
        A dict[email] = (firstname, surname)
    """
    with open(filepath, "r") as f:
        content = f.readlines()

    return [parse_contact(line, regex=contact_regex) for line in content]
