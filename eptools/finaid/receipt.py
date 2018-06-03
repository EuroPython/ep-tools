
"""
Functions to produce the financial aid receipt document
"""
from . import receipt_template_spa
from ..docstamp_utils import xelatex_document


def create_receipt(submission_data, template_file=None, output_dir="."):
    """ Call docstamp to use xelatex to produce a financial aid receipt
    for the application in `submission_data`. The output will be saved
    in output_dir.

    Parameters
    ----------
    submission_data: pandas.DataFrame
        A DataFrame with one row with the data of the applicant.
        Its columns must match the ones in the template_file content.

    template_file: str or pandas.DataFrame
        Path to the .tex template file.

    output_dir: str
        Path to the output folder.

    Returns
    -------
    output_path
    """

    def doclist_items(row):
        return "\n".join(["\item {}".format(doc) for doc in row["expense_docs"].split("\n")])

    def itemize_doclist(row):
        return "{}\n{}\n{}".format("\\begin{enumerate}", doclist_items(row), "\\end{enumerate}")

    submission_data["expense_docs"] = submission_data.apply(itemize_doclist, axis=1)

    if template_file is None:
        template_file = receipt_template_spa

    return xelatex_document(submission_data, template_file=template_file, field_name="full_name", output_dir=output_dir)
