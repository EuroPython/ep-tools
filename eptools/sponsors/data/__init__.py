"""
Declaration of the data files for the sponsors submodule.
"""
import os


module_dir = os.path.abspath(os.path.dirname(__file__))
contract_template = os.path.join(module_dir, "sponsor_agreement.tex")

# spreadsheet headers
billing_form_hdr = [
    "Timestamp",
    "Full comercial name",
    "Billing country",
    "Billing address",
    "Phone number",
    "Fax number",
    "VAT ID Number",
    "Others",
    "Full name",
    "ID Document",
    "ID Number",
    "Email",
    "Sponsorship Package",
    "Custom package",
    "Cost (without VAT)",
]

company_name_column = "Full comercial name"

control_ws_hdr = [
    "Sponsor",
    "Contact",
    "Manager",
    "AGREEMENT EPS/ACPySS",
    "contacted to fill form?",
    "sent agreement",
    "agreement signed",
    "put logo on web",
    "1st invoice sent",
    "1st invoice paid",
    "2dn invoice sent",
    "2nd invoice paid",
]
