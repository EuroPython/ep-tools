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
from   .data  import coordinates, scales, medal_files, badge_text_maxlength


def create_qrcode(contact, color, file_path):
    """return the file path to the svg file with a QRCode containing the contact VCard info."""
    vcard = dvcard.create_vcard3_str(name=contact.name,
                                     surname=contact.surname,
                                     displayname='',
                                     email=contact.email,
                                     org=contact.company,
                                     url=contact.persweb,
                                     note=contact.phone)
    save_into_qrcode(vcard, out_filepath=file_path, color=color)
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


def merge_badge_svgfiles(template_svgfile, pypower_svgfile, qrcode_svgfile, other_roles):
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

    other_roles: list of str
        Roles of the person to check if we have to add other 'medals' to the badge.
        E.g.: 'volunteer', 'epsmember'

    Returns
    -------
    SVG content
    """
    badge_svg = sg.fromfile(template_svgfile)

    # QRCODE
    # box_size: int
    #     Size of the QRCode.
    #     This is the value of the parameter `box_size` to create the
    #     QRCode in the function `docstamp.qrcode.save_into_qrcode`.
    qr         = sg.fromfile(qrcode_svgfile)
    qr_height  = float(qr.height.replace('mm', ''))
    qr_boxsize = scales.get('qrcode', 1)
    qr_coords  = coordinates['qrcode']

    qr_scale   = qr_boxsize/qr_height
    badge_svg  = merge_svg_files(badge_svg, qrcode_svgfile, qr_coords[0], qr_coords[1], scale=qr_scale)

    # TODO: clean up this function
    # PYPOWER
    if pypower_svgfile:
        svg_name = 'pypower'
        scale  = scales[svg_name]
        coords = coordinates[svg_name]
        badge_svg = merge_svg_files(badge_svg, pypower_svgfile, coords[0], coords[1], scale=scale)

    # EPSMEMBER
    if 'epsmember' in other_roles:
        svg_name  = 'epsmember'
        svg_file  = medal_files[svg_name]
        scale     = scales.get(svg_name, 1)
        coords    = coordinates[svg_name]
        badge_svg = merge_svg_files(badge_svg, svg_file, coords[0], coords[1], scale=scale)

    # VOLUNTEER
    if 'volunteer' in other_roles:
        svg_name  = 'volunteer'
        svg_file  = medal_files[svg_name]
        scale     = scales.get(svg_name, 1)
        coords    = coordinates[svg_name]
        badge_svg = merge_svg_files(badge_svg, svg_file, coords[0], coords[1], scale=scale)

    return badge_svg


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
        Example: 35
    """
    with open(badge_filepath) as f: svg = f.read()

    cid, _             = split_in_two(contact.id,      max_length=max_length)
    name, _            = split_in_two(contact.name,    max_length=max_length)
    surname, _         = split_in_two(contact.surname, max_length=max_length)
    tagline1, tagline2 = split_in_two(contact.tagline, max_length=max_length)
    company1, company2 = split_in_two(contact.company, max_length=max_length)

    svg = svg.replace('{{ name }}',     replace_chars_for_svg_code(name))
    svg = svg.replace('{{ surname }}',  replace_chars_for_svg_code(surname))
    svg = svg.replace('{{ tagline1 }}', replace_chars_for_svg_code(tagline1))
    svg = svg.replace('{{ tagline2 }}', replace_chars_for_svg_code(tagline2))
    svg = svg.replace('{{ company1 }}', replace_chars_for_svg_code(company1))
    svg = svg.replace('{{ company2 }}', replace_chars_for_svg_code(company2))
    svg = svg.replace('{{ id }}',       replace_chars_for_svg_code(cid))

    with open(badge_filepath, 'w') as f:
        f.write(svg)
