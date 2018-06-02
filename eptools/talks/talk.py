
"""
Functions to process talk data and its speakers.
"""
from collections import defaultdict


TALK_TYPE = (
    ("t_30", "Talk (30 mins)"),
    ("t_45", "Talk (45 mins)"),
    ("t_60", "Talk (60 mins)"),
    ("i_60", "Interactive (60 mins)"),
    ("r_180", "Training (180 mins)"),
    ("p_180", "Poster session (180 mins)"),
    ("n_60", "Panel (60 mins)"),
    ("n_90", "Panel (90 mins)"),
    ("h_180", "Help desk (180 mins)"),
)


TALK_CODE = {v: k for k, v in dict(TALK_TYPE).items()}

# Mapping of TALK_TYPE to duration in minutes
TALK_DURATION = {
    "t_30": 30,
    "t_45": 45,
    "t_60": 60,
    "i_60": 60,
    "r_180": 180,
    "p_180": 180,
    "n_60": 60,
    "n_90": 90,
    "h_180": 180,
}

TALK_ADMIN_TYPE = (
    ("o", "Opening session"),
    ("c", "Closing session"),
    ("l", "Lightning talk"),
    ("k", "Keynote"),
    ("r", "Recruiting session"),
    ("m", "EPS session"),
    ("s", "Open space"),
    ("e", "Social event"),
)


def get_talk_code(talk_type):
    return TALK_CODE.get(talk_type, None)


def get_speaker_type(talk_code):
    sym = talk_code.split("_")[0]
    if sym in ("t", "i", "p", "h", "n"):
        return "speaker"
    elif sym in ("r"):
        return "trainer"
    else:
        return None


def get_type_speakers(talks):
    """ Return a dictionary [type of speaker] -> list of emails.
    See ..talks.get_speaker_type and

    Parameters
    ----------
    talks: dict of talks
        dict[talk.id] -> talk dict
        From the talk_abstract.json file.
        Note that you have to remove the first key layer of the json content
        before using it as input to this function.

    Returns
    -------
    type_speaker: dict
        Type of speaker -> list of emails
    """
    type_speakers = defaultdict(list)
    for tid, talk in talks.items():
        stype = get_speaker_type(get_talk_code(talk["type"]))
        type_speakers[stype].extend(talk["emails"].split(", "))
    return type_speakers
