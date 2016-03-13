# coding: utf-8

"""
Helper functions to run commands on the epcon server.
"""
import os
import io
import os.path as op
import subprocess
import logging as log

from invoke import task

from .config import docker_name, epcon_db_path


def epcon_exe_manage(cmd, user='root', host='europython.io',
                     docker_name=docker_name):
    """ Run 'ssh `user`@`host` docker exec `doker_name` manage.py `cmd`'.
    Parameters
    ----------
    cmd: str
    user: str
    host: str
    docker_name: str

    Returns
    -------
    stdout: str
    """
    rmt_cmd = "ssh {}@{} docker exec {} python manage.py {}".format(user,
                                                                    host,
                                                                    docker_name,
                                                                    cmd)
    log.info('Running {}.'.format(rmt_cmd))
    proc = subprocess.Popen(rmt_cmd.split(' '), stdout=subprocess.PIPE)
    result = [x.decode('utf8') for x in proc.stdout.readlines()]
    return ''.join(result)


def epcon_fetch_file(cmd, fpath, user='root', host='europython.io'):
    """ Execute python manage.py command in epcon server to fetch a file.
    Will overwrite `fpath`. """
    if op.exists(fpath):
        os.remove(fpath)

    stdout = epcon_exe_manage(cmd=cmd, user=user, host=host)

    log.info('Writing output to {}.'.format(fpath))
    with io.open(fpath, 'w+') as f:
        f.write(stdout)

    return fpath


@task
def epcon_fetch_p3db(p3db_dirpath=epcon_db_path, out_dir='.', user='root', host='europython.io'):
    """ Download the p3.db file from the epcon server."""
    cmd = 'scp {}@{}:{} {}'.format(user, host, op.join(p3db_dirpath, 'p3.db'), out_dir)
    os.system(cmd)

