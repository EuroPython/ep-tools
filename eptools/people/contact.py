
import re
from enum import Enum
from collections import namedtuple


class AttendeeType(Enum):
    keynote = 'keynote'
    organizer = 'organizer'
    trainer = 'trainer'
    speaker = 'speaker'
    attendee = 'attendee'
    participant = 'participant'  # this is a British attendee
    trainee = 'trainee'


class TicketType(Enum):
    S = 'full'
    L = 'conference'
    D = 'daily'
    T = 'training'


class FareType(Enum):
    S = 'student'
    P = 'personal'
    C = 'company'


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
    "ticket_type",
    "fare_type",
)

Contact = namedtuple("Contact", CONTACT_FIELDS)

# TODO: for ep2019 we should use 'surname, name <email>' pattern. To match EPS membership list.

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
