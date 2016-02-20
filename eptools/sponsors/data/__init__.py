"""
Declaration of the data files for the sponsors submodule.
"""
import os.path as op


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

