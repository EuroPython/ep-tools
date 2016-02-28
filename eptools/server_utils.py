# coding: utf-8

"""
Helper functions to run commands on the epcon server.
"""

import os

from .config import docker_name


def epcon_exe_manage(cmd, user='root', host='epcon', docker_name=None):
    """ Run 'ssh `user`@`host` docker exec `doker_name` manage.py `cmd`'.
    Parameters
    ----------
    cmd: str
    user: str
    host: str
    docker_name: str
    """
    if docker_name is None:
        docker_name = docker_name

    os.system('ssh {}@{} docker exec {} python manage.py {}'.format(user,
                                                                    host,
                                                                    docker_name,
                                                                    cmd))


def epcon_fetch_file(cmd, fpath, user='root', host='epcon'):
    os.system('rm {}'.format(fpath))
    epcon_exe_manage(cmd='{} >> {}'.format(cmd, fpath),
                     user=user,
                     host=host)
    return fpath
