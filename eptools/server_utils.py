# coding: utf-8

"""
Helper functions to run commands on the epcon server.
"""

import os


def epcon_exe_manage(cmd, user='root', host='epcon'):
    os.system('ssh {}@{} docker exec arch_python_1 python manage.py {}'.format(user,
                                                                               host,
                                                                               cmd))


def epcon_fetch_file(cmd, fpath, user='root', host='epcon'):
    os.system('rm {}'.format(fpath))
    epcon_exe_manage(cmd='{} >> {}'.format(cmd, fpath),
                     user=user,
                     host=host)
    return fpath
