# coding: utf-8
"""
Functions to get the data Financial Aid submissions.
"""
from .data import finaid_submission_hdr
from ..gspread_utils import get_ws_data, find_one_row


def get_finaid_ws_data(api_key_file, doc_key, file_header=finaid_submission_hdr):
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
    return get_ws_data(api_key_file, doc_key,
                       ws_tab_idx=0,
                       header=file_header,
                       start_row=1)


def get_applicant(applicant_name, submissions, col_name='full_name'):
    """ Return a dict with the data of the applicant given his/her name
    and the content of the submissions form responses spreadsheet.

    Parameters
    ----------
    applicant_name: str
        This value will be used to search in the `col_name` of
        `finaid_ws_data`.
        This function looks for any cell with a `lower`-ed string
        that containts the `lower`-ed `applicant_name`.

    submissions: pandas.DataFrame
        Content of the submissions form responses spreadsheet.

    col_name: str
        Name of the column that holds the name of the applicants.

    Returns
    -------
    applicant: dict
    """
    return find_one_row(applicant_name, submissions, col_name=col_name)
