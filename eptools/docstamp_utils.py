
"""
Functions to help using docstamp.
"""

import os
import os.path as path


from docstamp.file_utils import get_extension, cleanup_docstamp_output
from docstamp.template import XeLateXDocument


def xelatex_document(doc_args, template_file, field_name, output_dir="."):
    """ Use docstamp to use xelatex to produce a XeLateX document
    using `template_file`.
    The output file will be saved in output_dir and its path returned.

    The doc_args keys will be lower case and have the white spaces replaced by '_'.

    Parameters
    ----------
    doc_args: dict or pandas.DataFrame
        A dictionary with the argument values to fill the `template_file`.

    template_file: str
        Path to the .tex template file.

    field_name: str
        Name of the field in `doc_args` that will be used for the
        output file name and some checks.

    output_dir: str
        Path to the output folder.

    Returns
    -------
    output_path

    """
    # input data
    def process_data_key(key):
        return key \
            .lower() \
            .replace(' ', '_') \
            .replace('(', '') \
            .replace(')', '')

    input_data = {process_data_key(key): value for key, value in doc_args.items()}

    # template doc
    template_doc = XeLateXDocument(template_file)

    # output file name
    field_val = input_data[process_data_key(field_name)].replace(" ", "")

    file_extension = get_extension(template_file)
    basename = path.basename(template_file).replace(file_extension, "")

    file_name = basename + "_" + field_val
    file_path = path.join(output_dir, file_name + ".pdf")

    # make output folder
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # fill the template
    template_doc.fill(input_data)

    # save into PDF
    template_doc.render(file_path)

    # clean up LateX mess
    cleanup_docstamp_output(output_dir)

    return file_path
