# coding: utf-8
"""
Helper functions read the participants data and generate all the badges.
"""
import os
import os.path as op

from   docstamp.inkscape   import svg2pdf
from   docstamp.pdf_utils  import merge_pdfs
from   docstamp.xml_utils  import change_xml_encoding

from .data import (
                   badge_files,
                   qrcode_color,
                   pythonpower_svg,
                   )

from .printer import (merge_badge_svgfiles,
                      fill_text_contact_badge,
                      create_qrcode,
                      )
from ..people.contact import ATTENDEE_TYPE


def create_badge_faces(pdf_filepath):
    """ duplicate the given pdf, save it in a file with '-joined.pdf' suffix and return the new filepath. """
    return merge_pdfs([pdf_filepath] * 2, pdf_filepath.replace('.pdf', '-joined.pdf'))


def get_badge_template_file(role):
    """ Return the path to the corresponding svg template file for the given
    participant ATTENDEE_TYPE."""
    return badge_files[role]


def get_badge_role(roles):
    """ Given a sequence of roles from the participant (can be strings or ATTENDEE_TYPE),
    will return the role that will appear in the person's badge."""
    for at in ATTENDEE_TYPE:
        if at.name in roles or at in roles or at.value in roles:
            return at

    return ATTENDEE_TYPE.attendee


def prepare_badge_pdf(svg_filepath):
    """ from the badge SVG file path prepare a PDF for printing. Returns the pdf file path. """
    pdf_filepath = svg_filepath.replace('.svg', '.pdf')

    svg2pdf(svg_filepath, pdf_filepath, dpi=300)

    pdf_pair_file = create_badge_faces(pdf_filepath)

    return pdf_pair_file


class BadgeFactory(object):
    """ Prepare the output folders and has the functions to create the badge SVG files in these folders. """
    def __init__(self, out_basedir):
        self.out_dir = ''
        self.tmp_dir = ''

        self.mkoutdirs(out_basedir)

    def mkoutdirs(self, out_basedir):
        if not op.exists(out_basedir):
            os.makedirs(out_basedir)

        out_dir = op.join(out_basedir, 'out')
        tmp_dir = op.join(out_basedir, 'tmp')

        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(tmp_dir, exist_ok=True)

        self.out_dir = out_dir
        self.tmp_dir = tmp_dir

    def _badge_filepath(self, contact, role, outdir, with_email=True, prefix='badge_ep2016'):
        """ Return the filepath to the corresponding svg file of the contact in the `outdir`
        folder.
        '{prefix}_{role}_{id}_{name}_{surname}_{emails}.svg'

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
        if with_email:
            fname_template = '{prefix}_{role}_{id}_{name}_{surname}_{emails}.svg'
        else:
            fname_template = '{prefix}_{role}_{id}_{name}_{surname}.svg'

        badge_filename = fname_template.format(prefix=prefix,
                                               role=role,
                                               id=contact.id,
                                               name=contact.name.replace      (' ', '' ),
                                               surname=contact.surname.replace(' ', '' ),
                                               emails=contact.email.replace    ('@', '.'),)
        return op.join(outdir, badge_filename)

    def _simple_badge_path(self, contact, role, outdir, prefix='badge_ep2016'):
        """ Return the filepath to the corresponding svg file of the contact in the `outdir`
        folder.
        '{prefix}_{role}_{id}.svg'

        Parameters
        ----------
        contact: Contact

        outdir: str
            Path to the output folder.


        prefix: str
            Prefix to include in the file name.

        Returns
        -------
        filepath: str
        """
        # badge name
        fname_template = '{prefix}_{role}_{id}.svg'

        badge_filename = fname_template.format(prefix=prefix,
                                               role=role,
                                               id=contact.id,)
        return op.join(outdir, badge_filename)

    def _badge_svg(self, contact, badge_role, other_roles, badge_template):
        """ return a badge svgfigure for the contact """
        pypower_file = ''
        if int(contact.pypower) > 0:
            pypower_file = pythonpower_svg[int(contact.pypower)]

        qrcode_file = op.join(self.tmp_dir, 'qrcode_{}.svg'.format(contact.email.replace('@', '.')))
        _ = create_qrcode(contact, color=qrcode_color[badge_role], file_path=qrcode_file)

        badge_svg = merge_badge_svgfiles(badge_template,
                                         pypower_file,
                                         qrcode_file,
                                         other_roles)

        return badge_svg

    def generate_badge_svg(self, contact, roles, badge_filepath=None):
        """ create a badge file for contact in outputdir. """
        #create badge image and save it
        role = get_badge_role(roles)
        template = get_badge_template_file(role)

        if badge_filepath is None:
            badge_filepath = self._simple_badge_path(contact,
                                                     role=role.name,
                                                     outdir=self.tmp_dir,)

        badge = self._badge_svg(contact, role, roles, template)
        badge.save(badge_filepath)

        change_xml_encoding(badge_filepath, 'ASCII', 'utf-8')
        fill_text_contact_badge(contact, badge_filepath)

        return badge_filepath
