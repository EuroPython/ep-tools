#!/usr/bin/env python


from random import randint
from time import sleep


def example_message(sender, recipients, greeting="Hello"):

    message = """
{greeting} {recipient_name},

Soy {sender_name} y lorem ipssum.

{sender_name}
""".format(
        sender_name=sender.name, recipient_name=recipients[0].name, greeting=greeting
    )

    subject = "EuroPython example message"

    return subject, message


def send_mail_msg(email_client, sender, recipients, subject, message, random_sleep=True):

    email_client.set_msg_header(sender, recipients, subject)
    email_client.set_msg_body_text(message)

    if random_sleep:
        sleep(randint(10, 100))

    email_client.send_email()


# if __name__ == "__main__":

# sender = EmailContact(*GMAIL_SENDER)
# client = get_gmail_client()

# send_email_to_known_international_companies        (sender)
