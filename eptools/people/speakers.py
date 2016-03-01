# coding: utf-8
"""
Functions to read talks data.
"""
from enum import Enum

from ..talks.fetch import talk_type, get_talk_type


def get_speakers_and_trainers(event_list):
    """

    Parameters
    ----------
    event_list

    Returns
    -------

    """
    speakers = set()
    trainers = set()
    for talk in event_list:
        talk_spkrs = talk['emails'].split(',')
        talk_type  = get_talk_type(talk)
        for speaker in talk_spkrs:
            speaker = speaker.strip()
            if talk_type is talk_type.talk:
                speakers.add(speaker)
            elif talk_type is talk_type.tutorial or talk_type is talk_type.helpdesk:
                trainers.add(speaker)

    return speakers, trainers


