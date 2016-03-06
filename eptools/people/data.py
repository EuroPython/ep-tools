# coding: utf-8
"""
A Borg that holds the records of the conference people data given a CSV file.
"""

import os.path as op
import json
from   collections import OrderedDict, defaultdict
from   operator    import itemgetter

from   docstamp.file_utils import csv_to_json

from .contact import CONTACT_FIELDS
from .contact import ATTENDEE_TYPE as roles
from .._utils import Borg


class ParticipantsRecords(Borg):
    """ Holds records of the participants and emails.
    """
    def __init__(self, participants_csv):
        super(ParticipantsRecords, self).__init__()

        self._people     = self._read_participants_csv(participants_csv)
        self.emails      = self.emails_dict()
        self.person_type = defaultdict(list)

    @staticmethod
    def _read_participants_csv(csv_file):
        json_file = op.join(op.dirname(csv_file), op.basename(csv_file).split('.')[:-1] + '.json')
        csv_to_json(csv_file, json_file, CONTACT_FIELDS)
        people = json.load(open(json_file, 'r'))
        return sorted(people, key=itemgetter('Name'))

    def emails_dict(self):
        return OrderedDict([(p['Email'], p) for p in self._people])

    def set_people_role(self, emails, role=roles.attendee):
        """ Set the roll of all the contacts in `emails` as `role`.
        Parameters
        ----------
        emails: list of str
            A list of email addresses.

        roll: ATTENDEE_TYPE
        """
        self.person_type[role].extend(emails)

    @staticmethod
    def role(self, email):
        """ Return the role of the participant given the person's email. """
        for role in list(roles):
            if email in self.emails_dict[role]:
                return role

        raise KeyError('Could not find role for {}.'.format(email))


# talks
SPEAKERS, TRAINERS = get_speakers_trainers(EVENTS)
KEYNOTERS          = read_email_list(op.join(DATA_DIR, 'keynoters.txt'))
ORGANIZERS         = read_email_list(op.join(DATA_DIR, 'organizers.txt'))

# create the files with the participants data
#DATAFILE           = op.join(DATA_DIR, ATTENDEES_CSV)
#csv_to_json(DATAFILE, ATTENDEES_JSON, CONTACT_FIELDS)
#ATTENDEES        = json.load(open(ATTENDEES_JSON, 'r'))
#SORTED_ATTENDEES = sorted(ATTENDEES, key=itemgetter('Name'))
#EMAIL_ATTENDEES  = OrderedDict([(p['Email'], p) for p in SORTED_ATTENDEES])

