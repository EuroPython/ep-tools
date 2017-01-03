"""
Functions to generate sponsor agreement documents.
"""

from .data import contract_template
from ..docstamp_utils import xelatex_document


def create_sponsor_agreement(sponsor_data, field_name='company',
                             template_file=None, output_dir='.'):
    """ Call docstamp to use xelatex to produce a sponsor agreement
    for the company in `sponsor_data`. The output will be saved
    in output_dir.

    Parameters
    ----------
    sponsor_data: pandas.DataFrame or dict
        A DataFrame with one row with the data of the sponsor.
        Its columns must match the ones in the template_file content.

    template_file: str
        Path to the .tex template file.

    output_dir: str
        Path to the output folder.

    Returns
    -------
    output_path

    """
    if template_file is None:
        template_file = contract_template

    if not isinstance(sponsor_data, dict):
        sponsor_data = sponsor_data.reset_index(drop=True).ix[0].to_dict()

    return xelatex_document(doc_args=sponsor_data,
                            field_name=field_name,
                            template_file=template_file,
                            output_dir=output_dir)
