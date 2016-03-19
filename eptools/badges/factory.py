# coding: utf-8
"""
Helper functions read the participants data and generate all the badges.
"""

import os
import os.path as op
import time
import shutil
import filecmp

from   docstamp.pdf_utils  import merge_pdfs
from   docstamp.inkscape   import svg2pdf
from   docstamp.qrcode     import save_into_qrcode
from   docstamp.xml_utils  import change_xml_encoding
import docstamp.vcard      as dvcard

from .printer import (merge_badge_svgfiles,
                      fill_text_contact_badge,
                      )

from .data import (
                   badge_files,
                   badge_color,
                   pythonpower_svg,
                   coordinates,
                   )

from .profiles import get_profiles_registry

from .._utils import Borg


class BadgeFactory(Borg):

    def __init__(self, out_basedir):
        super(BadgeFactory, self).__init__()

        self.out_dir = ''
        self.tmp_dir = ''

        self.mkoutdirs(out_basedir)

    def mkoutdirs(self, out_basedir):
        if not op.exists(out_basedir):
            raise IOError("Could not find the output base folder {}.".format(out_basedir))

        out_dir = op.join(out_basedir, 'out')
        tmp_dir = op.join(out_basedir, 'tmp')

        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(tmp_dir, exist_ok=True)

        self.out_dir = out_dir
        self.tmp_dir = tmp_dir

    @staticmethod
    def _template_file(attendee_email):
        """ Return the path to the corresponding svg template file for the given attendee."""
        return badge_files[people.role(attendee_email)]

    def _build_filepath(self, contact, outdir, with_email=True, prefix='badge_ep2016_'):
        """ Return the filepath to the corresponding svg file of the contact in the `outdir`
        folder.

        Parameters
        ----------
        contact: Contact

        outdir: str
            Path to the output folder.

        with_email: bool
            If True will include the emails address of the badge owner
            to the file name. False otherwise.

        prefix: str
            Prefix to include in the file name.

        Returns
        -------
        filepath: str
        """
        #badge name
        contact_type = people.role(contact.Email)
        if with_email:
            fname_template = '{prefix}_{type}_{name}_{surname}_{emails}.svg'
        else:
            fname_template = '{prefix}_{type}_{name}_{surname}.svg'

        badge_filename = fname_template.format(prefix=prefix,
                                               type=contact_type.name,
                                               name=contact.Name.replace      (' ', '' ),
                                               surname=contact.Surname.replace(' ', '' ),
                                               email=contact.Email.replace    ('@', '.'),)
        return op.join(outdir, badge_filename)


    def _badge_svg(self, contact):
        """ return a badge svgfigure for the contact """
        badge_template = self._template_file([people.role(contact.Email)])
        pypower_file   = pythonpower_svg[int(contact.Python_experience)]
        color          = badge_color[badge_template]
        vcard          = dvcard.create_vcard3_str(**dict(contact))

        qrcode_file    = op.join(self.tmp_dir,
                                 'qrcode_{}.svg'.format(contact.Email.replace('@', '.')))
        save_into_qrcode(vcard, qrcode_file, badge_color)

        return merge_badge_svgfiles(badge_template,
                                    pypower_file,
                                    qrcode_file,
                                    box_size=coordinates['qrcode_size'])


    def generate_contact_badge(self, contact, badge_filepath):
        """ create a badge file for contact in outputdir. """
        #create badge image and save it
        badge = self._badge_svg(contact)
        badge.save(badge_filepath)
        change_xml_encoding(badge_filepath, 'ASCII', 'utf-8')
        fill_text_contact_badge(contact, badge_filepath,
                                max_length=coordinates['badge_text_maxlength'])
        return badge


    def create_badge(self, contact, output_dir,  ):
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
