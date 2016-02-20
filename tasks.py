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

from eptools.finaid import (get_finaid_ws_data,
                            get_applicant,
                            receipt_template_spa,
                            create_receipt,
                           )

from eptools.config import (api_key_file,
                            sponsors_billing_worksheet,
                            finaid_submissions_worksheet,
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
        Can be a substring of the company name in the spreadsheet.

    template_file: str

    output_dir: str

    api_key_file: str
    """
    output_dir = op.abspath(output_dir)

    responses = get_sponsors_ws_data(api_key_file=api_key_file,
                                     doc_key=sponsors_billing_worksheet[0])

    try:
        sponsor_data = get_sponsor(sponsor_name=company_name,
                                   sponsors=responses,
                                   col_name='company')
    except:
        raise KeyError('Could not find data for sponsor {}.'.format(company_name))
    else:
        fpath = create_sponsor_agreement(sponsor_data,
                                         template_file=template_file,
                                         output_dir=output_dir)

        print('Created {}.'.format(fpath))


@task
def finaid_receipt(applicant_name, output_dir,
                   template_file=receipt_template_spa,
                   api_key_file=api_key_file):
    """ Call docstamp to produce a financial aid receipt
    for `applicant_name` using `template_file`.
    The output will be saved in `output_dir`.

    Parameters
    ----------
    applicant_name: str

    template_file: str

    output_dir: str

    api_key_file: str
    """
    output_dir = op.abspath(output_dir)

    responses = get_finaid_ws_data(api_key_file=api_key_file,
                                   doc_key=finaid_submissions_worksheet[0])

    try:
        applicant_data = get_applicant(applicant_name=applicant_name,
                                       submissions=responses,
                                       col_name='full_name')
    except:
        raise KeyError('Could not find data for applicant {}.'.format(applicant_name))
    else:
        fpath = create_receipt(applicant_data,
                               template_file=template_file,
                               output_dir=output_dir)

        print('Created {}.'.format(fpath))
