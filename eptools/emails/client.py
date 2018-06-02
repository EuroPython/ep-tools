
"""
Python emails clients
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.generator import Generator

try:
    # noinspection PyStatementEffect
    from email import Charset as charset
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
    from email import charset

# Default encoding mode set to Quoted Printable. Acts globally!
charset.add_charset("utf-8", charset.QP, charset.QP, "utf-8")

# from   credentials          import GMAIL_MAILADDR, GMAIL_PASSWORD, GMAIL_SENDER_NAME
# GMAIL_SENDER = (GMAIL_SENDER_NAME, GMAIL_MAILADDR)
#
# from   credentials          import PYSS_MAILADDR, PYSS_PASSWORD, PYSS_SENDER_NAME
# PYSS_SENDER = (PYSS_SENDER_NAME, PYSS_MAILADDR)


class EMailClient(object):

    _smtpserver = ""
    _serverport = ""

    def __init__(self, username, password, smtpserver="", serverport=""):
        self.username = username

        if not self._smtpserver:
            self._smtpserver = smtpserver

        if not self._serverport:
            self._serverport = serverport

        self.session = self.new_session()

        try:
            self.session.login(username, password)
        except Exception:
            print("Error trying to login with user {}.".format(username))
            raise

        self.message = None

    def new_session(self):
        try:
            session = smtplib.SMTP(self._smtpserver, self._serverport)
            session.ehlo()
            session.starttls()
        except Exception:
            raise
        else:
            return session

    @staticmethod
    def _get_email_contact_list(contacts):
        if contacts is not None:
            return ["{}".format(c) for c in contacts]

    def _add_addr_list(self, contacts, field="To"):
        self.msg[field] = ",".join(self._get_email_contact_list(contacts))

    def _add_from_addr(self, from_addr):
        self.msg["From"] = "{}".format(from_addr)

    def set_msg_header(self, from_addr, to_addr_list, subject, cc_addr_list=[]):
        # 'alternative’ MIME type – HTML and plain text bundled in one e-mail message
        self.msg = MIMEMultipart("alternative")
        self.msg["Subject"] = "{}".format(Header(subject, "utf-8"))

        # Only descriptive part of recipient and sender shall be encoded, not the emails address
        self._add_from_addr(from_addr)
        self._add_addr_list(to_addr_list, field="To")

        if cc_addr_list:
            self._add_addr_list(cc_addr_list, field="Cc")

    def set_msg_body_html(self, html):
        # Attach html parts
        htmlpart = MIMEText(html, "html", "UTF-8")
        self.msg.attach(htmlpart)

    def set_msg_body_text(self, text):
        # Attach text parts
        textpart = MIMEText(text, "plain", "UTF-8")
        self.msg.attach(textpart)

    def send_email(self):
        try:
            # Create a generator and flatten message object to 'file’
            str_io = StringIO()
            g = Generator(str_io, False)
            g.flatten(self.msg)

            # str_io.getvalue() contains ready to sent message
            # Optionally - send it – using python's smtplib
            problems = self.session.sendmail("", self.msg["To"], str_io.getvalue())

        except smtplib.SMTPException:
            print("Error: unable to send emails")
            print(problems)
            raise
        else:
            print("Successfully sent emails")


class GMailClient(EMailClient):
    _smtpserver = "smtp.gmail.com"
    _serverport = 587


class PySSMailClient(EMailClient):
    _smtpserver = "mail.pyss.org"
    _serverport = 465


class EmailContact(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '"{}" <{}>'.format(Header(self.name, "utf-8"), self.email)

    def __str__(self):
        return self.__repr__()
