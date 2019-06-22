"""
Functions to access the data in google drive spreadsheets
"""


def get_api_key_file():
    """ Return the api_key_file path imported from the config.py file"""
    try:
        from .config import api_key_file
    except ImportError:
        raise ImportError(
            "Could not find a path to the Google credentials file. "
            "You can set it up permanently in the config.py file."
        )
    else:
        return api_key_file


def get_ws_data(api_key_file, doc_key, ws_tab_idx, header=None, start_row=1):
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

    start_row: int
        Row index from where to start collecting the data.

    Returns
    -------
    content: pandas.DataFrame
    """
    import pandas as pd

    from eptools.gdrive import get_spreadsheet, worksheet_to_dict

    spread = get_spreadsheet(api_key_file, doc_key)
    ws = spread.get_worksheet(ws_tab_idx)

    ws_dict = worksheet_to_dict(ws, header=header, start_row=start_row)
    return pd.DataFrame(ws_dict)


def find_one_row(substr, df, col_name):
    """ Return one row from `df`. The returned row has in `col_name` column
    a value with a sub-string as `substr.

    Raise KeyError if no row is found.
    """
    for name in df[col_name]:
        if substr.lower() in name.lower():
            return df[df[col_name] == name]

    raise KeyError("Could not find {} in the " "pandas dataframe.".format(substr))
