
"""
Functions to download and process the sponsors billing data
"""

from .data import billing_form_hdr
from ..gspread_utils import get_ws_data, find_one_row


def get_sponsors_ws_data(api_key_file, doc_key, file_header=billing_form_hdr):
    """ Return the content of the Google Drive spreadsheet
    indicated by `doc_key`. `api_key_file` is the authentication
    file needed to access the document.

    The header of the data will be changed by `file_header`.
    Be careful because this header must be known to other functions here.

    Parameters
    ----------
    api_key_file: str
        Path to the Google credentials json file.

    doc_key: str
        Key for the document URL

    file_header: list of str
        List of ordered column names to rename the header of the spreadsheet
        data.

    Returns
    -------
    ws_data: pandas.DataFrame
    """
    return get_ws_data(api_key_file, doc_key, ws_tab_idx=0, header=file_header, start_row=1)


def get_sponsor(sponsor_name, sponsors, col_name="company"):
    """ Return a dict with the data of the sponsor given its name
    and the content of the billing form responses spreadsheet.

    Parameters
    ----------
    sponsor_name: str
        This value will be used to search in the `col_name` of
        `sponsor_ws_data`.
        This function looks for any cell with a `lower`-ed string
        that containts the `lower`-ed `sponsor_name`.

    sponsors: pandas.DataFrame
        Content of the billing form responses spreadsheet.

    col_name: str
        Name of the column that holds the name of the company.

    Returns
    -------
    sponsor: pandas.DataFrame
    """
    return find_one_row(sponsor_name, sponsors, col_name=col_name)
