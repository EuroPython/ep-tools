# coding: utf-8
"""
Functions to help using docstamp.
"""

import os
import os.path as op
import tempfile
import subprocess
import logging as log

from docstamp.file_utils import cleanup_docstamp_output


def create_document(df, template_file, field_name, index=None, output_dir='.'):
    """ Call docstamp to use xelatex to produce a XeLateX document
    using `template_file`.
    The output file will be saved in output_dir.

    #TODO: instead of using docstamp from a syscall, why not import docstamp itself?

    Parameters
    ----------
    df: pandas.DataFrame
        A DataFrame with one row with the data to fill the template_file.
        Its columns must match the ones in the template_file content.
        If df has more than one row, make sure you set a value for `index`.

    template_file: str
        Path to the .tex template file.

    index: int
        The row index in `df` if it has more than one row.

    field_name: str
        Name of the field in `row_data` that will be used for the
        output file name and some checks.

    output_dir: str
        Path to the output folder.

    Returns
    -------
    output_path

    """
    if index is None:
        if len(df) != 1:
            raise ValueError('Expected either `df` with one row or a value for `index`, '
                             ' none of those.')
        else:
            index = 0

    fd, path = tempfile.mkstemp()
    df.to_csv(path)

    cmd  = 'docstamp'
    cmd += ' -i "{data_file}"'
    cmd += ' -t "{template}"'
    cmd += ' -o "{output_dir}"'
    cmd += ' -f "{field_name}"'
    cmd += ' -c xelatex'
    cmd += ' --idx "{index}"'
    cmd += ' -v'
    cmd = cmd.format(data_file=path,
                     template=template_file,
                     output_dir=output_dir,
                     field_name=field_name,
                     index=index)

    log.info('Calling {}'.format(cmd))

    oldcwd = op.abspath(op.curdir)
    os.chdir(op.dirname(template_file))

    subprocess.call(cmd, shell=True)

    os.chdir(oldcwd)

    cleanup_docstamp_output(output_dir)

    item_name = df[field_name].values[index].strip().replace(' ', '_')
    return op.join(output_dir, '{}_{}.pdf'.format(op.basename(template_file),
                                                  item_name))
