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
    env.hosts = ['35.237.202.116', '34.73.195.113']

    if not path.exists(archive_path):
        return False

    # send archive
    result = put(archive_path, "/tmp/")
    if result.failed:
        return False

    # save names
    arch = archive_path.split('/')[1].split('.')[0]
    archDir = "/data/web_static/releases/".apend(arch)
    remote_path = "/temp/{}".format(archive_path.split('/')[1])

    # make dir
    run("mkdir -p /data/web_static/releases/{}".format(arch))

    # uncompress the archive
    # -x: Extract files from an archive
    # -z: Uncompress whit gzip command
    # -f: use archive file or device ARCHIVE
    # -C: Change to directory.
    result = run(
        "tar -xzf {} -C {}".format(remote_path, archDir))
    if result.failed:
        return False

    # delete the archive
    result = run("rm {}".format(remote_path))
    if result.failed:
        return False

    # move files
    result = run("mv {}/web_static/* {}".format(archDir, archDir))
    if result.failed:
        return False

    result = run("rm -rf {}/web_static".format(archDir))
    if result.failed:
        return False

    # softlink to new deploy
    result = run("rm - rf / data/web_static/current")
    if result.failed:
        return False

    result = run(
        "ln -sf {} /data/web_static/current".format(archDir))
    if result.failed:
        return False

    return True
