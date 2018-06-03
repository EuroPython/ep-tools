
"""
A class that holds the records of the conference people data given a CSV file.
"""
import itertools
from copy import deepcopy
from collections import defaultdict
from operator import itemgetter


def clean_name(name):
    return name.lower().strip()


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
        self.people = sorted(profiles, key=itemgetter("id"))
        self.role_emails = defaultdict(list)
        self.role_names = defaultdict(list)

    def set_emails_role(self, emails, role):
        """ Set the roll of all the contacts in `emails` as `role`.
        Parameters
        ----------
        emails: list of str
            A list of emails addresses.

        role: str
            The default is 'participant' but you can add whatever you need.
        """
        self.role_emails[role].extend(emails)

    def set_names_role(self, names, role):
        """ Set the roll of all the contacts in `emails` as `role`.
        Parameters
        ----------
        names: list of 2-tuple of str
            A list of 2-tuple (name, surname).

        role: str
            The default is 'participant' but you can add whatever you need.
        """
        lownames = [(clean_name(n), clean_name(s)) for n, s in deepcopy(names)]
        self.role_names[role].extend(lownames)

    def get_roles_of(self, email, name="", surname=""):
        """ Return the roles of the participant given the person's email,
        name_surname is optional."""
        emails_roles = (role_name for role_name, roles in self.role_emails.items() if email in roles)
        names_roles = (
            role_name
            for role_name, roles in self.role_names.items()
            if (clean_name(name), clean_name(surname)) in roles
        )
        return set(itertools.chain(emails_roles, names_roles))

    def difference(self, other, key_field="id"):
        """ Return the profiles in `other` that are different from the ones in
        self. """
        pr1 = self.people.copy()

        diff = []
        pr2 = {p[key_field]: p for p in other.people}
        for p in pr1:
            p2 = pr2[p[key_field]]
            if p == p2:
                roles1 = self.get_roles_of(p["email"], p["name"], p["surname"])
                roles2 = other.get_roles_of(p["email"], p["name"], p["surname"])
                if roles1 != roles2:
                    diff.append(p)
            else:
                diff.append(p)
        return diff

    def __iter__(self):
        yield from self.people
