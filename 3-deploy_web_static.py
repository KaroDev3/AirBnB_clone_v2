#!/usr/bin/python3
"""
3. Full deployment
Script that creates and distributes an archive to web servers,
using the function deploy
"""
from fabric.operations import local, run, put, env
from os import path
import datetime

env.hosts = ['35.237.202.116', '34.73.195.113']
env.user = 'ubuntu'


def do_pack():
    """ Fabric script that generates a .tgz archive from
    the contents of the web_static """
    local("mkdir -p versions")
    date = datetime.datetime.now()
    date_format = date.strftime("%Y%m%d%H%M%S")
    new_archive = local(
        "tar -cvzf versions/web_static_{}.tgz web_static".format(date_format))
    if new_archive.succeeded:
        return "versions/web_static_{}.tgz".format(date_format)
    else:
        return None


def do_deploy(archive_path):
    """ Deploy archive """

    if not path.exists(archive_path):
        return False

    # send archive
    put(archive_path, "/tmp/")

    # save names
    arch = archive_path.split('/')[1].split('.')[0]
    archDir = "/data/web_static/releases/" + arch
    remote_path = "/tmp/{}".format(archive_path.split('/')[1])

    # make dir
    run("mkdir -p {}".format(archDir))

    # uncompress the archive
    # -x: Extract files from an archive
    # -z: Uncompress whit gzip command
    # -f: use archive file or device ARCHIVE
    # -C: Change to directory.
    run("tar -xzf {} -C {}/".format(remote_path, archDir))

    # delete the archive
    run("rm {}".format(remote_path))

    # move files
    run("mv {}/web_static/* {}".format(archDir, archDir))

    run("rm -rf {}/web_static".format(archDir))

    # softlink to new deploy
    run("rm -rf /data/web_static/current")

    run("ln -s {}/ /data/web_static/current".format(archDir))

    return True


def deploy():
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
