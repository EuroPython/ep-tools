# coding: utf-8

import re
from   copy import copy
from   enum import Enum
from   collections import namedtuple


# Define attendee types
ATTENDEE_TYPE = Enum('Attendee_Type', 'keynote organizer trainer speaker attendee')
TALK_TYPE     = Enum('Talk_Type',     'talk tutorial helpdesk')

# contact class
CONTACT_FIELDS = ("Name", "Surname", "Tagline", "Affiliation", "Python_experience",
                  "T_shirt", "Email", "Phone", "Company_homepage", "Personal_homepage")

Contact = namedtuple('Contact', CONTACT_FIELDS)


def create_contact(person_info):
    person = copy(person_info)
    person['Personal_homepage'] = person['Personal_homepage'].replace('http://', '')
    person['Company_homepage']  = person['Company_homepage'].replace('http://', '')
    if not person['Affiliation']:
        person['Affiliation'] = person['Company_homepage']

    #for field in person:
    #    person[field] = to_str(person[field])

    return Contact(**person)


def parse_email_contact(email_str):
    """ Parse a string in the format '<name, surname> email'
    Returns
    -------
    given_name, family_name, email: str
    """
    pattern = re.compile(r"<(?P<name>.*),(?P<surname>.*)>(?P<email>.*@.*)")
    try:
        matches = pattern.match(email_str)
    except:
        raise ValueError('Error reading email in line {}.'.format(email_str))
    else:
        return matches.groups()


def parse_email_contact_fmt2(email_str):
    """ Parse a string in the format 'Name Surname <email>'
    Returns
    -------
    given_name, family_name, email: str
    """
    pattern = re.compile(r"^(?P<name>[\S]*)[ ]*?(?P<surname>.*)[ ]*?<(?P<email>.*@.*)>.*?$")
    try:
        matches = pattern.match(email_str)
    except:
        raise ValueError('Error reading email in line {}.'.format(email_str))
    else:
        return matches.groups()


def get_contacts(strlist):
    """ Parse a list of contact strings `strlist` into a dict[email]->(name, surname).

    Parameters
    ----------
    strlist: list of str

    Returns
    -------
    emails: dict
        A dict[email] = (firstname, surname)
    """
    if strlist is None:
        return {}

    contacts = [parse_email_contact(line) for line in strlist]
    emails   = {email: (name, surname) for name, surname, email in contacts}

    return emails


def read_contacts_file(filepath):
    """ Read a list of contacts from a text file in `filepath`.
    The contact format is: <FirstName, SurName> EmailAddress

    Parameters
    ----------
    filepath: str
        Path to the input file

    Returns
    -------
    emails: dict
        A dict[email] = (firstname, surname)
    """
    with open(filepath, 'r') as f:
        content = f.readlines()

    return get_contacts(content)


