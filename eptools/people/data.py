"""
A Borg that holds the records of the conference people data given a CSV file.
"""
import os.path as op
import json
from   collections import OrderedDict, defaultdict
from   operator    import itemgetter

from   docstamp.file_utils import csv_to_json

from .contact import CONTACT_FIELDS, ATTENDEE_TYPE

class Borg:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
    # and whatever else you want in your class -- that's all!


class ParticipantsRecords(Borg):
    """ Holds records of the participants and emails.
    """
    def __init__(self, participants_csv):
        super(ParticipantsRecords, self).__init__()

        self._data = self._read_participants_csv(participants_csv)
        self.emails = self.emails_dict()
        self.person_type = defaultdict(list)

    def _read_participants_csv(self, csv_file):
        json_file = op.join(op.dirname(csv_file), op.basename(csv_file).split('.')[:-1] + '.json')
        csv_to_json(csv_file, json_file, CONTACT_FIELDS)
        participants = json.load(open(json_file, 'r'))
        return sorted(participants, key=itemgetter('Name'))

    def emails_dict(self):
        return OrderedDict([(p['Email'], p) for p in self.participants])

    def set_people_kind(self, emails, type):
        """

        Parameters
        ----------
        emails: list of str
            A list of email addresses.

        type: ATTENDEE_TYPE
        """
        self.person_type[type].extend(emails)

    def get_person_type(self, email):
        """ Return the type of participant given the person's email. """
        if email in KEYNOTERS:
            return ATTENDEE_TYPE.keynote
        elif email in ORGANIZERS:
            return ATTENDEE_TYPE.organizer
        elif email in TRAINERS:
            return ATTENDEE_TYPE.trainer
        elif email in SPEAKERS:
            return ATTENDEE_TYPE.speaker
        else:
            return ATTENDEE_TYPE.attendee

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

