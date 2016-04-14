# coding: utf-8
"""
Helper functions to add content and setup one badge file.
"""
import svgutils.transform as sg
from   docstamp.svg_utils import merge_svg_files, replace_chars_for_svg_code
from   docstamp.pdf_utils import merge_pdfs
from   docstamp.qrcode    import save_into_qrcode
import docstamp.vcard     as dvcard

from   .utils import split_in_two
from   .data  import coordinates


def create_qrcode(contact, color, file_path):
    """return the file path to the svg file with a QRCode containing the contact VCard info."""
    vcard = dvcard.create_vcard3_str(name=contact.name,
                                     surname=contact.surname,
                                     displayname='',
                                     email=contact.email,
                                     org=contact.company,
                                     url=contact.persweb,
                                     note=contact.phone)
    save_into_qrcode(vcard, file_path, color)
    return file_path


def duplicate_badge_file(pdf_filepath, suffix='-joined'):
    """ Create a PDF file with 2 consecutive copies of `pdf_filepath`.

    Parameters
    ----------
    pdf_filepath: str
        Path to the PDF file path.

    suffix: str
        Suffix for the new file name.

    Returns
    -------
    out_path: str
        Path to the merged file path.
    """
    return merge_pdfs([pdf_filepath]*2, pdf_filepath.replace('.pdf', suffix + '.pdf'))


def _add_python_power(badge_svgfile, pypower_svgfile, coords, scale):
    """ Add the pypower_svgfile to the badge svg.

    Parameters
    ----------
    badge_svgfile: str
        Path to the SVG file.

    pypower_svgfile: str
        Path to the SVG file.

    coords: 2-tuple of int
        Example: (STARS_X, STARS_Y)

    scale: float
        Example: STARS_SCALE

    Returns
    -------
    SVG content
    """
    bg = sg.fromfile(badge_svgfile)
    badge_height = float(bg.get_size()[1])
    return merge_svg_files(badge_svgfile, pypower_svgfile, coords[0], badge_height - coords[1], scale=scale)


def _add_qrcode(badge_svgfile, qrcode_svgfile, coords, box_size=10):
    """ Add a QRCode SVG content to badge_svg.

    Parameters
    ----------
    badge_svgfile: str
        Path to the SVG file.

    qrcode_svgfile: str
        Path to the SVG file

    box_size: int
        Size of the QRCode.
        This is the value of the parameter `box_size` to create the
        QRCode in the function `docstamp.qrcode.save_into_qrcode`.

    coords: 2-tuple of int
        Example: (STARS_X, STARS_Y)

    scale: float
        Example: STARS_SCALE

    Returns
    -------
    SVG content
    """
    #print(qr.get_size())
    #qr.set_size(('57mm', '57mm'))
    qr = sg.fromfile(qrcode_svgfile)
    bg = sg.fromfile(badge_svgfile)
    qr_height = float(qr.height.replace('mm', ''))
    badge_height = float(bg.get_size()[1])
    scale = box_size/qr_height

    return merge_svg_files(badge_svgfile, qrcode_svgfile, coords[0], badge_height - coords[1], scale=scale)


def merge_badge_svgfiles(template_svgfile, pypower_svgfile, qrcode_svgfile, box_size=10):
    """ Merge pypower_file and qrcode_file contents into the correct position
    in the badge file template_svgfile.

    Parameters
    ----------
    template_svgfile: str
        Path to the badge template file.

    pypower_svgfile: str
        Path to the Python Power stars svg file.

    qrcode_svgfile: str
        Path to the SVG file.

    box_size: int
        Size of the QRCode.
        This is the value of the parameter `box_size` to create the
        QRCode in the function `docstamp.qrcode.save_into_qrcode`.

    Returns
    -------
    SVG content
    """
    #bg = sg.fromfile(template_svgfile)
    stars_coords = (coordinates['stars_x'], coordinates['stars_y'])
    stars_scale  = coordinates['stars_scale']
    bg = _add_python_power(template_svgfile, pypower_svgfile, coords=stars_coords, scale=stars_scale)

    qrcode_coords = (coordinates['qrcode_x'], coordinates['qrcode_y'])
    bg = _add_qrcode(template_svgfile,  qrcode_svgfile, coords=qrcode_coords, box_size=box_size)

    return bg


def tshirt_code(tshirt_string):
    """ convert tshirt size strings into a code for us"""
    if not tshirt_string:
        return ''

    tshirt_code = ''
    if tshirt_string[0] == 'f':
        tshirt_code += '0'
        tshirt_string = tshirt_string[1:]
    else:
        tshirt_code += '1'

    size_code = {'s'  : '1',
                 'm'  : '2',
                 'l'  : '3',
                 'xl' : '4',
                 'xxl': '5',
                 '3xl': '6',
                 '4xl': '7',}
    tshirt_code += size_code.get(tshirt_string, '')
    return tshirt_code


def fill_text_contact_badge(contact, badge_filepath, max_length):
    """ Fill the contact information in the template badge file.

    contact: .people.Contact

    badge_filepath: str
        Path to the template badge file.

    max_length: int
        Maximum number of characters of text allowed in the template fields.
        This does not take into account the font type/size.
        This number should be checked manually filling the badge.
        Example: BADGE_TEXT_MAXLENGTH
    """
    with open(badge_filepath) as f: svg = f.read()

    name, _            = split_in_two(contact.name,        max_length=max_length)
    surname, _         = split_in_two(contact.surname,     max_length=max_length)
    tagline1, tagline2 = split_in_two(contact.tagline,     max_length=max_length)
    org1, org2         = split_in_two(contact.company,     max_length=max_length)
    shirt_code         = tshirt_code(contact.tshirt)

    svg = svg.replace('{{ name }}',    replace_chars_for_svg_code(name))
    svg = svg.replace('{{ surname }}', replace_chars_for_svg_code(surname))
    svg = svg.replace('{{ tagline }}', replace_chars_for_svg_code(tagline1))
    svg = svg.replace('{{ org1 }}',    replace_chars_for_svg_code(org1))
    svg = svg.replace('{{ org2 }}',    replace_chars_for_svg_code(org2))
    svg = svg.replace('{{ tshirt }}',  replace_chars_for_svg_code(shirt_code))

    with open(badge_filepath, 'w') as f:
        f.write(svg)
