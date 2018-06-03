"""
Declaration of the data files for the financial aid submodule.
"""
import os.path as op

module_dir = op.abspath(op.dirname(__file__))
receipt_template_spa = op.join(module_dir, "acpyss_recibi_spa.tex")

# spreadsheet headers
finaid_submission_hdr = ["full_name", "amount", "amount_script", "expense_docs", "address"]
