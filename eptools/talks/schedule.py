# coding: utf-8
"""
Helper functions to manage the conference schedule.
"""
from invoke import task

from ..server_utils import epcon_exe_manage


@task
def check_schedule(ctx, what='all_scheduled', conf='ep2017'):
    """ Check if all accepted talks are scheduled and if all scheduled talks
    are accepted.
    Choices for 'what': ('all_scheduled', 'all_accepted').
    """
    cmd = 'check_schedule {conf} --{what}'.format(conf=conf, what=what)
    stdout = epcon_exe_manage(cmd)

    if not stdout.strip():
        print('Everything is alright.')
    else:
        print(stdout)
