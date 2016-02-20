# coding: utf-8
"""
Helper functions read the participants data and generate all the badges.
"""

import os
import os.path as op
import time
import json
import shutil
import filecmp
from   collections   import OrderedDict
from   operator      import itemgetter

from   docstamp.file_utils import csv_to_json
from   docstamp.pdf_utils  import merge_pdfs
from   docstamp.inkscape   import svg2pdf
from   docstamp.qrcode     import save_into_qrcode
from   docstamp.xml_utils  import change_xml_encoding

from .printer import (merge_badge_svgfiles,
                      fill_text_contact_badge,
                      )

# from .people import (get_speakers_trainers,
#                      read_email_list,
#                      create_contact,
#                      )


# from .people import (
#                      CONTACT_FIELDS,
#                      ATTENDEE_TYPE,
#                      )


# talks

SPEAKERS, TRAINERS = get_speakers_trainers(EVENTS)
KEYNOTERS          = read_email_list(op.join(DATA_DIR, 'keynoters.txt'))
ORGANIZERS         = read_email_list(op.join(DATA_DIR, 'organizers.txt'))

# create the files with the participants data
DATAFILE           = op.join(DATA_DIR, ATTENDEES_CSV)
csv_to_json(DATAFILE, ATTENDEES_JSON, CONTACT_FIELDS)
ATTENDEES        = json.load(open(ATTENDEES_JSON, 'r'))
SORTED_ATTENDEES = sorted(ATTENDEES, key=itemgetter('Name'))
EMAIL_ATTENDEES  = OrderedDict([(p['Email'], p) for p in SORTED_ATTENDEES])


def get_attendee_type(contact_email):
    """  """
    email = contact_email
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



ATTENDEE_BADGETYPE = {ATTENDEE_TYPE.keynote  : KEYNOTE_BADGEFILE,
                      ATTENDEE_TYPE.organizer: ORGANIZER_BADGEFILE,
                      ATTENDEE_TYPE.trainer  : TRAINER_BADGEFILE,
                      ATTENDEE_TYPE.speaker  : SPEAKER_BADGEFILE,
                      ATTENDEE_TYPE.attendee : ATTENDEE_BADGEFILE,
                     }

BADGE_COLOR = {KEYNOTE_BADGEFILE:   'e37500',
               ORGANIZER_BADGEFILE: 'bc445c',
               TRAINER_BADGEFILE:   '5e9e90',
               SPEAKER_BADGEFILE:   'a98700', #'e2b000',
               ATTENDEE_BADGEFILE:  'a3150e'}




def mkoutdirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TRASH_DIR, exist_ok=True)


def badge_template_for(attendee_email):
    """ Return the path to the corresponding svg template file for the given attendee."""
    return ATTENDEE_BADGETYPE[get_attendee_type(attendee_email)]


def badge_filename(contact, outdir, with_email=True, prefix='badge_ep2016_'):
    """ Return the filepath to the corresponding svg file of the contact in the `outdir`
    folder.

    Parameters
    ----------
    contact: Contact

    outdir: str

    with_email: bool

    prefix: str

    Returns
    -------
    filepath: str
    """
    #badge name
    contact_type = get_attendee_type(contact.Email)
    if with_email:
        fname_template = '{prefix}_{type}_{name}_{surname}_{email}.svg'
    else:
        fname_template = '{prefix}_{type}_{name}_{surname}.svg'

    badge_filename = fname_template.format(prefix=prefix,
                                           type=contact_type.name,
                                           name=contact.Name.replace      (' ', '' ),
                                           surname=contact.Surname.replace(' ', '' ),
                                           email=contact.Email.replace    ('@', '.'),)
    return op.join(outdir, badge_filename)


def create_badge_svg(contact):
    """ return a badge svgfigure for the contact """
    badge_template = ATTENDEE_BADGETYPE[get_attendee_type(contact.Email)]
    pypower_file   = PYTHONPOWER_SVG[int(contact.Python_experience)]
    badge_color    = BADGE_COLOR[badge_template]
    vcard          = vcard_text(contact)

    qrcode_file    = op.join(TRASH_DIR,
                             'qrcode_{}.svg'.format(contact.Email.replace('@', '.')))
    save_into_qrcode(vcard, qrcode_file, badge_color)

    return merge_badge_svgfiles(badge_template,
                                pypower_file,
                                qrcode_file,
                                box_size=QRCODE_SIZE)


def generate_contact_badge(contact, badge_filepath):
    """ create a badge file for contact in outputdir. """
    #create badge image and save it
    badge = create_badge_svg(contact)
    badge.save(badge_filepath)
    change_xml_encoding(badge_filepath, 'ASCII', 'utf-8')
    fill_text_contact_badge(contact, badge_filepath, max_length=BADGE_TEXT_MAXLENGTH)
    return badge


def create_badge_pdf(contact, output_dir,  ):
    """

    Parameters
    ----------
    contact

    Returns
    -------

    """
    CONTACT = create_contact(ATTENDEE)

    if not get_attendee_type(CONTACT.Email) is BADGE_TYPE:
        continue

    badge_filepath = get_badge_filename(CONTACT, output_dir, with_email=True)
    pdf_filepath   = badge_filepath.replace('.svg', '.pdf')

    TEST_BADGE = False
    if CHECK_IF_EXIST:
        # if check will create a new file and compare it to the old one.
        if op.exists(pdf_filepath):
            ORIG_BADGE_FILEPATH = badge_filepath
            ORIG_PDF_FILEPATH   = pdf_filepath
            BADGE_FILEPATH      = badge_filepath.replace('.svg', '.2.svg')
            pdf_filepath        = pdf_filepath.replace  ('.pdf', '.2.pdf')
            TEST_BADGE = True

    # generate pdf file
    generate_contact_badge(CONTACT, badge_filepath)
    svg2pdf(badge_filepath, pdf_filepath, dpi=300) #, inkscape_binpath=INKSCAPE_BINPATH)

    time.sleep(3)
    os.remove(badge_filepath)

    #check if the generated if the same as the old one
    if TEST_BADGE:
        if not filecmp.cmp (pdf_filepath, ORIG_PDF_FILEPATH, shallow=False):
            shutil.copyfile(pdf_filepath, ORIG_PDF_FILEPATH)
            os.remove      (pdf_filepath)
            PDF_FILEPATH  = ORIG_PDF_FILEPATH
        else:
            os.remove(pdf_filepath)
            continue

    #create pair-of-badges pdf
    PDF_PAIR_FILE = create_badge_faces(PDF_FILEPATH)
    BADGE_FILEPATHS.append(PDF_PAIR_FILE)
    print(BADGE_FILEPATH)



# In[18]:

CHECK_IF_EXIST = False
BADGE_TYPE = ATTENDEE_TYPE.speaker
BADGE_FILEPATHS = []

BADGE_OUTPUT_DIR = op.join(OUTPUT_DIR, BADGE_TYPE.name)
mkdir(BADGE_OUTPUT_DIR)


for ATTENDEE in SORTED_ATTENDEES:
    create_contact_badge(contact)
    # CONTACT = create_contact(ATTENDEE)
    #
    # if not get_attendee_type(CONTACT.Email) is BADGE_TYPE:
    #     continue
    #
    # BADGE_FILEPATH = get_badge_filename(CONTACT, BADGE_OUTPUT_DIR, with_email=True)
    # PDF_FILEPATH   = BADGE_FILEPATH.replace('.svg', '.pdf')
    #
    # TEST_BADGE = False
    # if CHECK_IF_EXIST:
    #     # if check will create a new file and compare it to the old one.
    #     if op.exists(PDF_FILEPATH):
    #         ORIG_BADGE_FILEPATH = BADGE_FILEPATH
    #         ORIG_PDF_FILEPATH   = PDF_FILEPATH
    #         BADGE_FILEPATH      = BADGE_FILEPATH.replace('.svg', '.2.svg')
    #         PDF_FILEPATH        = PDF_FILEPATH.replace  ('.pdf', '.2.pdf')
    #         TEST_BADGE = True
    #
    # # generate pdf file
    # generate_contact_badge(CONTACT, BADGE_FILEPATH)
    # PDF_FILEPATH = prepare_badge_for_print(BADGE_FILEPATH, PDF_FILEPATH)
    # time.sleep(3)
    # os.remove(BADGE_FILEPATH)
    #
    # #check if the generated if the same as the old one
    # if TEST_BADGE:
    #     if not filecmp.cmp (PDF_FILEPATH, ORIG_PDF_FILEPATH, shallow=False):
    #         shutil.copyfile(PDF_FILEPATH, ORIG_PDF_FILEPATH)
    #         os.remove      (PDF_FILEPATH)
    #         PDF_FILEPATH  = ORIG_PDF_FILEPATH
    #     else:
    #         os.remove(PDF_FILEPATH)
    #         continue
    #
    # #create pair-of-badges pdf
    # PDF_PAIR_FILE = create_badge_faces(PDF_FILEPATH)
    # BADGE_FILEPATHS.append(PDF_PAIR_FILE)
    # print(BADGE_FILEPATH)


if BADGE_FILEPATHS:
    BADGES_LIST_FILE = op.join(OUTPUT_DIR, '{}_badges.pdf'.format(BADGE_TYPE.name))
    print('Merging {} badges.'.format(len(BADGE_FILEPATHS)))
    print(BADGES_LIST_FILE)
    merge_pdfs(BADGE_FILEPATHS, BADGES_LIST_FILE)
else:
    print('No badges to make.')


# In[ ]:
