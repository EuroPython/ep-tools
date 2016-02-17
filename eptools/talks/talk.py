# coding: utf-8
"""
Functions to process data of one talk.
"""
from   enum import Enum

# Define attendee types
talk_type     = Enum('Talk_Type', 'talk tutorial poster helpdesk')
# talk_duration = {'talk': 30,
#                  '',
#                 }
talk_durations = {30, 45, 60}


def is_talk(event):
    """    """
    return (event['duration'] in talk_durations)


def get_talk_type(slot_event):
    """    """
    return talk_type.talk if is_talk(slot_event) else talk_type.tutorial

