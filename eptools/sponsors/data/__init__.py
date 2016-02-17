"""
Functions and imports to access the data files for the sponsors submodule.
"""
import os.path as op

import pandas as pd

from   docstamp.gdrive import (get_spreadsheet,
                               worksheet_to_dict)


module_dir        = op.abspath(op.dirname(__file__))
contract_template = op.join(module_dir, 'sponsor_agreement_1invoice.tex')

# spreadsheet headers
billing_form_hdr  = ['date', 'company', 'country', 'address',
                     'vat', 'Others', 'representative',
                     'identification', 'document', 'email',
                     'services', 'price', 'VAT']

control_ws_hdr = ['Sponsor', 'Contact', 'Manager',
                  'AGREEMENT EPS/ACPySS',
                  'contacted to fill form?',
                  'sent agreement',
                  'agreement signed',
                  'put logo on web',
                  '1st invoice sent',
                  '1st invoice paid',
                  '2dn invoice sent',
                  '2nd invoice paid']


def get_sponsor(sponsor_name, sponsors, col_name='company'):
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
    sponsor: dict
    """
    for name in sponsors[col_name]:
        if sponsor_name.lower() in name.lower():
            return sponsors[sponsors[col_name] == name]
    else:
        raise KeyError('Could not find sponsor {} in the '
                       'sponsors responses spreadsheet.'.format(sponsor_name))


def get_ws_data(api_key_file, doc_key, ws_tab_idx, header=None):
    """ Return the content of the spreadsheet in the ws_tab_idx tab of
    the spreadsheet with doc_key as a pandas DataFrame.

    Parameters
    ----------
    api_key_file: str
        Path to the Google API key json file.

    doc_key: str

    ws_tab_idx: int
        Index of the worksheet within the spreadsheet.

    header: List[str]
        List of values to assign to the header of the result.

    Returns
    -------
    content: pandas.DataFrame
    """
    spread = get_spreadsheet(api_key_file, doc_key)
    ws     = spread.get_worksheet(ws_tab_idx)

    ws_dict = worksheet_to_dict(ws, header=header, start_row=1)
    return pd.DataFrame(ws_dict)


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
    return get_ws_data(api_key_file, doc_key, ws_tab_idx=0, header=file_header)
