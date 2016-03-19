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

# regexes
email_regex = r"[\w0-9\.\+\_\-]+@[\w0-9\.\+\_\-]+\.\w+"

#'<name, surname> email'
contact_regex1 = r"^<(?P<name>[\w0-9\. ]+),[ ]?((?P<surname>[\w0-9\. ]+))>[ ]?(?P<email>{email})?$".format(email=email_regex)

# name, surname <email>
contact_regex2 = "^(?P<name>[\w0-9\.\_\- ]+)[ ]*,[ ]*(?P<surname>[\w0-9\. ]+)([ ]*<(?P<email>{email})>)?$".format(email=email_regex)


def create_contact(person_info):
    person = copy(person_info)
    person['Personal_homepage'] = person['Personal_homepage'].replace('http://', '')
    person['Company_homepage']  = person['Company_homepage'].replace('http://', '')
    if not person['Affiliation']:
        person['Affiliation'] = person['Company_homepage']

    #for field in person:
    #    person[field] = to_str(person[field])

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
        raise ValueError('Error reading contact in line {}.'.format(string))

    m = matches.groupdict()
    return m['name'], m['surname'], m['email']


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


