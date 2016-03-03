#!/usr/bin/env python
#coding: utf-8

from   random               import randint
from   time                 import sleep


from .client import GMailClient


def example_message(sender, recipients, greeting='Hello'):

    message = """
{greeting} {recipient_name},

Soy {sender_name} y lorem ipssum.

{sender_name}
""".format(sender_name=sender.name, recipient_name=recipients[0].name, greeting=greeting)

    subject = 'EuroPython example message'

    return subject, message


def send_mail_msg(email_client, sender, recipients, subject, message, random_sleep=True):

    email_client.set_msg_header    (sender, recipients, subject)
    email_client.set_msg_body_text (message)

    if random_sleep:
        sleep(randint(10, 100))

    email_client.send_email()


def read_gspread(doc_key, worksheet_name=''):

    gc = get_google_auth()

    #Go to Google Sheets and share your spreadsheet with an email you have in your json_key['client_email'].
    #Otherwise you’ll get a SpreadsheetNotFound exception when trying to open it.
    spread   = gc.open_by_key(doc_key)

    try:
        if worksheet_name:
            wks = spread.worksheet(worksheet_name)
        else:
            wks = spread.sheet1
    except:
        wks  = spread.sheet1

    all_rows = wks.get_all_values()
    keys     = all_rows[0]
    data     = [dict(zip(keys, values)) for values in all_rows[1:]]

    return data


if __name__ == '__main__':

    sender = EmailContact(*GMAIL_SENDER)
    client = get_gmail_client()

    #send_email_to_known_international_companies        (sender)
