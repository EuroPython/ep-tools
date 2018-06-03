"""
Invoke tasks to be run from the command line.
"""
import os
from invoke import task

from eptools.gspread_utils import get_api_key_file
from eptools.talks import fetch_talks_json as _fetch_talks
from eptools.people import fetch_ticket_profiles as _fetch_profiles

from eptools.config import sponsors_billing_worksheet, finaid_submissions_worksheet


@task
def sponsor_agreement(ctx, company_name, output_dir, template_file="", api_key_file=""):
    """ Call docstamp to produce a sponsor agreement for `company_name`
    using `template_file`. The output will be saved in `output_dir`.

    Parameters
    ----------
    company_name: str
        Can be a substring of the company name in the spreadsheet.

    template_file: str

    output_dir: str

    api_key_file: str
        The path to the Google Credentials json file.
        If left empty will try to look for its path in the config.py file.
    """

    from eptools.sponsors import (
        get_sponsor,
        get_sponsors_ws_data,
        create_sponsor_agreement,
        contract_template,
        company_name_column,
    )

    if not template_file:
        template_file = contract_template

    if not api_key_file:
        api_key_file = get_api_key_file()

    output_dir = os.path.abspath(output_dir)

    responses = get_sponsors_ws_data(api_key_file=api_key_file, doc_key=sponsors_billing_worksheet[0])

    try:
        sponsor_data = get_sponsor(sponsor_name=company_name, sponsors=responses, col_name=company_name_column)
    except Exception:
        raise KeyError("Could not find data for sponsor {}.".format(company_name))
    else:
        fpath = create_sponsor_agreement(sponsor_data, template_file=template_file, output_dir=output_dir)

        print("Created {}.".format(fpath))


@task
def finaid_receipt(ctx, applicant_name, output_dir, template_file="", api_key_file=""):
    """ Call docstamp to produce a financial aid receipt
    for `applicant_name` using `template_file`.
    The output will be saved in `output_dir`.

    Parameters
    ----------
    applicant_name: str

    template_file: str

    output_dir: str

    api_key_file: str
        Path to the Google credentials json file.
        If left empty will try to look for its path in the config.py file.
    """

    from eptools.finaid import get_finaid_ws_data, get_applicant, receipt_template_spa, create_receipt

    if not template_file:
        template_file = receipt_template_spa

    if not api_key_file:
        api_key_file = get_api_key_file()

    output_dir = os.path.abspath(output_dir)

    responses = get_finaid_ws_data(api_key_file=api_key_file, doc_key=finaid_submissions_worksheet[0])

    try:
        applicant_data = get_applicant(applicant_name=applicant_name, submissions=responses, col_name="full_name")
    except Exception:
        raise KeyError("Could not find data for applicant {}.".format(applicant_name))
    else:
        fpath = create_receipt(applicant_data, template_file=template_file, output_dir=output_dir)

        print("Created {}.".format(fpath))


@task
def fetch_ticket_profiles(ctx, out_filepath, conf="ep2017", status="all", nondups=False, raise_=False, ticket_id=""):
    """ Create a json file with the all the tickets of the conference.
        make_option('--status',
                    choices=['all', 'complete', 'incomplete'],
                    help='Status of the orders related with the tickets.',
        make_option('--nondups',
                    help='If enables will remove the tickets with '
                         'same owner/email.',
        make_option('--raise',
                    help='If enabled will raise any error that it may find.',
        make_option('--ticket-id',
                    help='Will output the profile of the given ticket only.',
    """
    return _fetch_profiles(out_filepath, conf=conf, status=status, nondups=nondups, raise_=raise_, ticket_id=ticket_id)


@task
def fetch_talks_json(ctx, out_filepath="", status="proposed", conf="ep2017", host="europython.io", with_votes=False):
    """ Return the talks in a json format. `status` choices: ['accepted', 'proposed']
    """
    return _fetch_talks(out_filepath=out_filepath, status=status, conf=conf, host=host, with_votes=with_votes)
