"""
Helper functions to add content and setup one badge file.
"""

from docstamp.pdf_utils import merge_pdfs
from docstamp.qrcode import save_into_qrcode
import docstamp.vcard as dvcard

from eptools.config import conference


def create_qrcode(contact, color, file_path):
    """Return the file path to the svg file with a QRCode containing the contact VCard info."""
    vcard = dvcard.create_vcard3_str(
        name=contact.name,
        surname=contact.surname,
        displayname="",
        email=contact.email,
        org=contact.company,
        title=contact.title,
        url=contact.persweb,
        note="EuroPython {}".format(conference[-4:]),
    )
    save_into_qrcode(vcard, out_filepath=file_path, color=color)
    return file_path


def duplicate_badge_file(pdf_filepath, suffix="-joined"):
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
    return merge_pdfs([pdf_filepath] * 2, pdf_filepath.replace(".pdf", suffix + ".pdf"))


def tshirt_code(tshirt_string):
    """ convert tshirt size strings into a code for us"""
    if not tshirt_string:
        return ""

    tshirt_code = ""
    if tshirt_string[0] == "f":
        tshirt_code += "0"
        tshirt_string = tshirt_string[1:]
    else:
        tshirt_code += "1"

    size_code = {"s": "1", "m": "2", "l": "3", "xl": "4", "xxl": "5", "3xl": "6", "4xl": "7"}
    tshirt_code += size_code.get(tshirt_string, "")
    return tshirt_code
