
"""
Helper functions to manage the conference schedule.
"""
from invoke import task

from eptools import config
from eptools.server_utils import epcon_exe_manage


@task
def check_schedule(ctx, what="all_scheduled", conference=None):
    """ Check if all accepted talks are scheduled and if all scheduled talks
    are accepted.
    Choices for 'what': ('all_scheduled', 'all_accepted').
    """
    if conference is None:
        conference = config.conference

    cmd = "check_schedule {conference} --{what}".format(conference=conference, what=what)
    stdout = epcon_exe_manage(cmd)

    if not stdout.strip():
        print("Everything is alright.")
    else:
        print(stdout)
