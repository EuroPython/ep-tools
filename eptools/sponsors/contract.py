
import os
import os.path as op
import tempfile
import subprocess
import logging as log

#import pandas as pd
from docstamp.file_utils import cleanup_docstamp_output

from . import contract_template


def create_sponsor_agreement(sponsor_data, template_file=None, output_dir='.'):
    """ Call docstamp to use xelatex to produce a sponsor agreement
    for the company in `sponsor_data`. The output will be saved
    in output_dir.

    Parameters
    ----------
    sponsor_data: pandas.DataFrame
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
    fd, path = tempfile.mkstemp()
    sponsor_data.to_csv(path)

    if template_file is None:
        template_file = contract_template
    #sponsor_idx = 0
    #company_name       = data[0]['company']

    cmd  = 'docstamp'
    cmd += ' -i "{data_file}"'
    cmd += ' -t "{template}"'
    cmd += ' -o "{output_dir}"'
    cmd += ' -f company'
    cmd += ' -c xelatex'
    cmd += ' --idx 0'
    cmd += ' -v'
    cmd = cmd.format(data_file=path,
                     template=template_file,
                     output_dir=output_dir)

    log.debug('Calling {}'.format(cmd))

    oldcwd = op.abspath(op.curdir)
    os.chdir(op.dirname(template_file))

    subprocess.call(cmd, shell=True)

    os.chdir(oldcwd)

    cleanup_docstamp_output(output_dir)

    company_name = sponsor_data['company'].values[0].strip()

    return op.join(output_dir, '{}_{}.pdf'.format(op.basename(template_file),
                                                  company_name))
