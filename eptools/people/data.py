# coding: utf-8
"""
A Borg that holds the records of the conference people data given a CSV file.
"""
from collections import defaultdict
from operator    import itemgetter


class ParticipantsRegistry(object):
    """ Holds records of the participants and emails.
    Parameters
    ----------
    profiles: list of dicts of str
        Each profile with this minimal structure:
         {u'email': u'',
          u'name': u'',
          u'surname': u'',
          ...},
    """
    def __init__(self, profiles):
        self._people     = sorted(profiles, key=itemgetter('email'))
        self.role_emails = defaultdict(list)

    def set_people_role(self, emails, role):
        """ Set the roll of all the contacts in `emails` as `role`.
        Parameters
        ----------
        emails: list of str
            A list of emails addresses.

        role: str
            The default is 'participant' but you can add whatever you need.
        """
        self.role_emails[role].extend(emails)

    def get_roles_of(self, email):
        """ Return the roles of the participant given the person's email. """
        return (role for role in self.role_emails if email in self.role_emails[role])
