#!/usr/bin/python3
""" 2. Deploy archive!
Fabric script that distributes an archive to web servers,
using the function do_deploy
"""
from fabric.api import *
from os import path


def do_deploy(archive_path):
    """ Deploy archive """

    env.user = 'ubuntu'
    env.hosts = ['localhost']

    if not path.exists(archive_path):
        return False

    """ send archive """
    result = put(archive_path, "/tmp/")
    if result.failed:
        return False

    filename = archive_path.split('/')
    filename = filename[len(filename) - 1].split('.')[0]
    remote_path = "/data/".apend(filename)

    """ uncompress the archive """
    run("mkdir -p /data/web_static/releases/")
    result = run(
        "tar -xzf {} -C /data/web_static/releases/".format(remote_path))
    if result.failed:
        return False

    """ delete the archive """
    result = run("rm {}".format(remote_path))
    if result.failed:
        return False

    """ softlink to new deploy """
    run("rm /data/web_static/current")
    result = run(
        "ln -sf /data/web_static/releases/{}\
             /data/web_static/current".format(filename))

    return True
