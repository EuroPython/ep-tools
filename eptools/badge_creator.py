
# coding: utf-8

# In[5]:


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# In[6]:


""" Outer interface to produce conference badge files. """

import json
import os
import subprocess
import logging

from eptools.config import conference
from eptools.people.fetch import fetch_ticket_profiles
from eptools.people.profiles import load_id_json
from eptools.talks.fetch import fetch_talks_json
from eptools._utils import ParameterGrid


OUTPUT_DIR = os.path.expanduser("badges")

LOGGER = logging.getLogger("badge_maker")


# In[7]:


# Fetch data
fetch_data = False
talks_file = "accepted_talks.json"
profiles_file = "profiles.json"

# fetch the data from the DB
if fetch_data:
    fetch_ticket_profiles(profiles_file, conference=conference)
    fetch_talks_json(talks_file, conference=conference, status="accepted", with_votes=True)

logger.info(f"Created raw data files in {profiles_file} and {talks_file}.")


# In[8]:


people = load_id_json(profiles_file, add_id=True)


# In[9]:


# add speaker statuses ['speaker_type'] -> (None, 'speaker', 'trainer')
from enum import Enum
from collections import defaultdict

from eptools.badges.printer import tshirt_code
from eptools.people.profiles import read_contacts
from eptools.people.contact import AttendeeType
from eptools.talks.talk import TALK_CODE, get_speaker_type
from eptools.badges.utils import split_in_two


class SpeakerType(Enum):
    speaker = "speaker"
    trainer = "trainer"
    keynote_speaker = "keynote_speaker"


class TicketType(Enum):
    training = "training"
    conference = "conference"


class FareType(Enum):
    student = "student"
    personal = "personal"
    business = "business"


# put all talks in a id -> talk dictionary
conference_talks = {}
types_talks = dict(json.load(open(talks_file)).items())
for ttype, talkset in types_talks.items():
    conference_talks.update(talkset)

# add a type_code fielt to understand the type of code
for id, talk in conference_talks.items():
    talk["type_code"] = TALK_CODE[talk["type"]]

# create a dict email -> list of talk type
speaker_talks = defaultdict(set)
for id, talk in conference_talks.items():
    emails = talk["emails"].split(", ")
    speaker_type = get_speaker_type(talk["type_code"])
    for email in emails:
        speaker_talks[email].add(speaker_type)

for person in people:
    speaker_type = speaker_talks.get(person["email"], None)
    if speaker_type:
        if "trainer" in speaker_type:
            speaker_type = SpeakerType.trainer
        else:
            speaker_type = SpeakerType.speaker
    person["speaker_type"] = speaker_type


# In[10]:


# add keynote statuses ['speaker_type'] -> ('keynote')
keynote_speakers_emails = {person[2] for person in read_contacts("keynoters.txt")}
for person in people:
    if person["email"] in keynote_speakers_emails:
        person["speaker_type"] = SpeakerType.keynote_speaker


# In[11]:


# add participant type statuses ['ticket_type'] -> ('conference', 'training')
for person in people:
    fare_code = person["fare_code"]
    if fare_code.startswith("TRT"):
        person["ticket_type"] = TicketType.training
    else:
        person["ticket_type"] = TicketType.conference


# In[12]:


# add organizer status ['epsmember'] -> (True, False)
organizers_emails = {person[2] for person in read_contacts("organizers.txt")}

for person in people:
    person["is_organizer"] = person["email"] in organizers_emails


# In[13]:


for person in people:
    if person["is_organizer"]:
        badge_type = AttendeeType.organizer

    elif person["speaker_type"] == SpeakerType.keynote_speaker:
        badge_type = AttendeeType.keynote

    elif person["speaker_type"] == SpeakerType.trainer:
        badge_type = AttendeeType.trainer

    elif person["speaker_type"] == SpeakerType.speaker:
        badge_type = AttendeeType.speaker

    elif person["ticket_type"] == TicketType.training:
        badge_type = AttendeeType.trainee

    elif person["ticket_type"] == TicketType.conference:
        badge_type = AttendeeType.attendee

    person["badge_type"] = badge_type


# In[14]:


# add ticket type status ['fare_type'] -> ('student', 'personal', 'business')
for person in people:
    fare_code = person["fare_code"]
    if fare_code.endswith("S"):
        fare_type = FareType.student
        person["company"] = ""
    elif fare_code.endswith("P"):
        fare_type = FareType.personal
        person["company"] = ""
    elif fare_code.endswith("C"):
        fare_type = FareType.business
    else:
        raise ValueError("Expected a valid FareType code, but got {}.".format(fare_code))

    person["fare_type"] = fare_type.value


# In[11]:


# add python power as star string: ★
for person in people:
    person["python_power"] = "Python power: " + "★" * person["pypower"] if person["pypower"] else ""


# In[12]:


# add epsmembership status ['is_epsmember'] -> (True, False)
epsmembers_emails = {person[2] for person in read_contacts("epsmembers.txt")}

for person in people:
    person["is_epsmember"] = person["email"] in epsmembers_emails


# In[13]:


# add volunteer status ['is_volunteer'] -> (True, False)
volunteers_emails = {person[2] for person in read_contacts("volunteers.txt")}

for person in people:
    person["is_volunteer"] = person["email"] in volunteers_emails


# In[14]:


# add tshirt code
for person in people:
    person["tshirt_code"] = tshirt_code(person["tshirt"])


# In[15]:


# add qrcode content: vcard
import docstamp.vcard as dvcard


def person_vcard(person: dict) -> str:
    """Return the file path to the svg file with a QRCode containing the contact VCard info."""
    vcard = dvcard.create_vcard3_str(
        name=person["name"],
        surname=person["surname"],
        displayname="",
        email=person["email"],
        org=person["company"],
        title=person["title"],
        url=person["persweb"],
        note="EuroPython {}".format(conference[-4:]),
    )
    return vcard


for person in people:
    person["vcard"] = person_vcard(person)


# In[16]:


from eptools.badges.data import module_dir, badge_files, medal_files, coordinates, scales, maxlengths

# fix entries for maximum length, only tagline for now
for person in people:
    person["tagline1"], person["tagline2"] = split_in_two(person["tagline"], max_length=maxlengths["tagline"])


# In[17]:


# add data to pick the right badge template


def badges_trait_as_string(badges_trait: dict) -> str:
    return "_".join(("{}-{}".format(trait, value) for trait, value in badges_trait.items() if trait != "badge_type"))


badges_traits = {
    "badge_type": {person["badge_type"] for person in people},
    "is_epsmember": {person["is_epsmember"] for person in people},
    "is_volunteer": {person["is_volunteer"] for person in people},
}

badges_traits_grid = tuple(ParameterGrid(badges_traits))
num_traits = len(badges_traits)

peoples_traits = defaultdict(list)
for person in people:
    for idx, badges_trait in enumerate(badges_traits_grid):
        shared_items = {k: person[k] for k in person if k in badges_trait and person[k] == badges_trait[k]}
        if len(shared_items) == num_traits:
            peoples_traits[idx].append(person)


# In[18]:


assert sum(len(people_traits) for _, people_traits in peoples_traits.items()) == len(people)


# In[19]:


# generate template files
from typing import Union

import svgutils.transform as sg
from docstamp.svg_utils import merge_svg_files, _check_svg_file
from docstamp.xml_utils import change_xml_encoding


docstamp_dir = os.path.join(module_dir, conference, "docstamp")
os.makedirs(docstamp_dir, exist_ok=True)


def _add_epsmember_medal(badge_svg: Union[str, sg.SVGFigure]) -> sg.SVGFigure:
    svg_name = "epsmember"
    svg_file = medal_files[svg_name]
    scale = scales.get(svg_name, 1)
    coords = coordinates[svg_name]
    return merge_svg_files(badge_svg, svg_file, coords[0], coords[1], scale=scale)


def _add_volunteer_medal(badge_svg: Union[str, sg.SVGFigure]) -> sg.SVGFigure:
    svg_name = "volunteer"
    svg_file = medal_files[svg_name]
    scale = scales.get(svg_name, 1)
    coords = coordinates[svg_name]
    return merge_svg_files(badge_svg, svg_file, coords[0], coords[1], scale=scale)


for badges_trait in badges_traits_grid:
    badge_type = badges_trait["badge_type"]

    output_badge_file = os.path.basename(badge_files[badge_type]).replace(".svg", "")
    output_badge_file += "_" + badges_trait_as_string(badges_trait) + ".svg"
    output_badge_file = os.path.join(docstamp_dir, output_badge_file)
    logger.info(f"Generating badge template: {output_badge_file}.")

    original_badge_file = badge_files[badge_type]

    output_badge_svg = _check_svg_file(original_badge_file)
    if badges_trait["is_epsmember"]:
        output_badge_svg = _add_epsmember_medal(output_badge_svg)

    if badges_trait["is_volunteer"]:
        output_badge_svg = _add_volunteer_medal(output_badge_svg)

    output_badge_svg.save(output_badge_file)
    change_xml_encoding(output_badge_file, "ASCII", "utf-8")


# In[20]:


import pandas as pd

for idx, people_traits in peoples_traits.items():
    df = pd.DataFrame(people_traits)

    badge_trait = badges_traits_grid[idx]
    badge_type = badge_trait["badge_type"]

    badge_file_name = os.path.basename(badge_files[badge_type]).replace(".svg", "")
    csv_file = badge_file_name + "_" + badges_trait_as_string(badge_trait) + ".csv"
    logger.info(f"Creating data file: {csv_file}.")
    df.to_csv(os.path.join(docstamp_dir, csv_file), index=False)


# In[21]:


from glob import glob

docstamp_output_dir = os.path.join(docstamp_dir, "stamped")


def docstamp(input_file, outdir, template_file, naming_field="id"):
    cmd = 'docstamp create -i "{}" -t "{}" -f "{}" -d svg -o "{}" -v'.format(
        input_file, template_file, naming_field, outdir
    )
    logger.debug(f"Calling {cmd}")
    subprocess.check_call(shlex.split(cmd))


for csv_file in glob(os.path.join(docstamp_dir, "*.csv")):
    logger.info(f"Docstamping: {csv_file}.")

    badge_template_file = csv_file.replace(".csv", ".svg")
    assert os.path.exists(badge_template_file)

    docstamp(csv_file, docstamp_output_dir, badge_template_file, naming_field="id")


# In[22]:


# qrcode-related helpers

import tempfile

import svgutils.transform as sg
import qrcode
import qrcode.image.svg
from docstamp.file_utils import replace_file_content

from eptools.badges.data.parameters import qrcode_color


def _text_to_qrcode_svg(text: str, box_size: int = 1) -> qrcode.image.svg.SvgPathImage:
    """ Return `text` in a qrcode svg object.

    Parameters
    ----------
    text: str
        The string to be codified in the QR image.

    box_size: scalar
        Size of the QR code boxes.

    Returns
    -------
    qrcode: svg
    """
    try:
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box_size)
        qr.add_data(text)
        qr.make(fit=True)
    except Exception as exc:
        raise Exception("Error trying to generate QR code " " from `vcard_string`: {}".format(text)) from exc
    else:
        img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)

    return img


def qrcode_to_svgfigure(qrcode: qrcode.image.svg.SvgPathImage, color: str = "") -> sg.SVGFigure:
    tmp_file = tempfile.NamedTemporaryFile(mode="w+b", delete=True)
    qrcode.save(tmp_file.name)
    if color:
        replace_file_content(tmp_file.name, "fill:#000000", "fill:#{}".format(color))
    return sg.fromfile(tmp_file.name)


def _add_qrcode(badge_svg: Union[str, sg.SVGFigure], qrcode_svg: Union[str, sg.SVGFigure]) -> sg.SVGFigure:
    qr_height = float(qrcode_svg.height.replace("mm", ""))
    qr_boxsize = scales.get("qrcode", 1)
    qr_coords = coordinates["qrcode"]
    qr_scale = qr_boxsize / qr_height
    return merge_svg_files(badge_svg, qrcode_svg, qr_coords[0], qr_coords[1], scale=qr_scale)


def get_person_qrcode_figure(person):
    qrcode = _text_to_qrcode_svg(person["vcard"])
    return qrcode_to_svgfigure(qrcode, color=qrcode_color[person["badge_type"]])


def person_badge_base_filename(person: dict) -> str:
    return "_".join(("{}-{}".format(trait, person[trait]) for trait in badges_traits if trait != "badge_type"))


for person in people:
    badge_file_name = os.path.basename(badge_files[person["badge_type"]]).replace(".svg", "")
    badge_file_name += "_" + person_badge_base_filename(person)
    badge_file_name += "_" + str(person["id"])
    badge_file_name += ".svg"

    badge_filepath = os.path.join(docstamp_output_dir, badge_file_name)
    logger.debug(f"Adding QR code to {badge_filepath}.")
    assert os.path.exists(badge_filepath)

    qrcode_figure = get_person_qrcode_figure(person)

    badge_figure = _add_qrcode(badge_filepath, qrcode_figure)
    badge_figure.save(badge_filepath)


# In[ ]:

from glob import glob
from docstamp.inkscape import svg2pdf


for svg_file in glob(os.path.join(docstamp_output_dir, "*.svg")):
    logger.info(f"Converting {svg_file} to PDF.")
    svg2pdf(svg_file, svg_file.replace(".svg", ".pdf"), dpi=150)
    os.remove(svg_file)


# In[ ]:

import shlex


def pdf_to_cmyk(input_file: str, output_file: str):
    cmd = (
        "gs -dSAFER -dBATCH -dNOPAUSE -dNOCACHE -sDEVICE=pdfwrite "
        "-sColorConversionStrategy=CMYK "
        "-dProcessColorModel=/DeviceCMYK "
        '-sOutputFile="{}" "{}"'.format(output_file, input_file)
    )
    logger.info(f"Calling: {cmd}")
    subprocess.call(shlex.split(cmd))


for pdf_file in glob(os.path.join(docstamp_output_dir, "*.pdf")):
    logger.info(f"Changing color scheme to CMYK of {pdf_file}.")
    pdf_to_cmyk(pdf_file, pdf_file.replace(".pdf", "_cmyk.pdf"))
    os.remove(pdf_file)
