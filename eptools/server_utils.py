# coding: utf-8

"""
Helper functions to run commands on the epcon server.
"""
import os
import os.path as op
import logging as log

from invoke import task

from .config import docker_name, epcon_db_path


def epcon_exe_manage(cmd, user='root', host='epcon', docker_name=docker_name):
    """ Run 'ssh `user`@`host` docker exec `doker_name` manage.py `cmd`'.
    Parameters
    ----------
    cmd: str
    user: str
    host: str
    docker_name: str
    """
    rmt_cmd = 'ssh {}@{} docker exec {} python manage.py {}'.format(user,
                                                                    host,
                                                                    docker_name,
                                                                    cmd)
    log.info('Running {}.'.format(rmt_cmd))
    os.system(rmt_cmd)


def epcon_fetch_file(cmd, fpath, user='root', host='epcon'):
    """ Execute python manage.py command in epcon server to fetch a file. Will overwrite `fpath`. """
    if op.exists(fpath):
        os.remove(fpath)

    epcon_exe_manage(cmd='{} >> {}'.format(cmd, fpath),
                     user=user,
                     host=host)
    return fpath


@task
def epcon_fetch_p3db(p3db_dirpath=epcon_db_path, out_dir='.', user='root', host='epcon'):
    """ Download the p3.db file from the epcon server."""
    cmd = 'scp {}@{}:{} {}'.format(user, host, op.join(p3db_dirpath, 'p3.db'), out_dir)
    os.system(cmd)

