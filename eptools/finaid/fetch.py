# coding: utf-8
"""
Functions to get the data Financial Aid submissions.
"""
from ..server_utils import epcon_fetch_file



from .fetch import billing_form_hdr
from ..gspread import get_ws_data


def get_sponsors_ws_data(api_key_file, doc_key, file_header=billing_form_hdr):
    """ Return the content of the Google Drive spreadsheet
    indicated by `doc_key`. `api_key_file` is the authentication
    file needed to access the document.

    Get the data of the Financial Aid submissions.

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



def fetch_finaid_submissions(out_filepath, conf='ep2016'):
    """ Create csv file with the data of the Financial Aid submissions. """
    return epcon_fetch_file(cmd='get_attendees_csv {} {}'.format(conf, 'complete'),
                            fpath=out_filepath)


def fetch_ticketless_csv(out_filepath, conf='ep2016'):
    """ Create csv file with participants without ticket.  """
    return epcon_fetch_file(cmd='get_attendees_csv {} {}'.format(conf, 'incomplete'),
                            fpath=out_filepath)
