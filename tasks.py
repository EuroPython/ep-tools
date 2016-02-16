"""
Invoke tasks to be run from the command line.
"""
import os.path as op
from invoke import task

from eptools.sponsors import (get_sponsor,
                              get_sponsors_ws_data,
                              create_sponsor_agreement,
                              contract_template,
                              )

from eptools.ep2016_config import (api_key_file,
                                   sponsors_billing_worksheet,
                                   )


@task
def sponsor_agreement(company_name, output_dir,
                      template_file=contract_template,
                      api_key_file=api_key_file):
    """ Call docstamp to produce a sponsor agreement for `company_name`
    using `template_file`. The output will be saved in `output_dir`.

    Parameters
    ----------
    company_name: str

    template_file: str

    output_dir: str

    api_key_file: str
    """
    output_dir = op.abspath(output_dir)

    responses = get_sponsors_ws_data(api_key_file=api_key_file,
                                     doc_key=sponsors_billing_worksheet[0])

    sponsor_data = get_sponsor(sponsor_name=company_name,
                               sponsors=responses,
                               col_name='company')

    if sponsor_data is None:
        raise KeyError('Could not find data for sponsor {}.'.format(company_name))

    if template_file is None:
        template_file = contract_template

    fpath = create_sponsor_agreement(sponsor_data,
                                     template_file=template_file,
                                     output_dir=output_dir)

    print('Created {}.'.format(fpath))
