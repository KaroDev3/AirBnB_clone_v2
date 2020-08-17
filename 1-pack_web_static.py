#!/usr/bin/python3
""" 1. Compress before sending
script that generates a .tgz archive from thecontents of the web_static
"""
from fabric.api import local
import datetime


def do_pack():
    """ Fabric script that generates a .tgz archive from
    the contents of the web_static """
    local("mkdir -p versions")
    date = datetime.datetime.now()
    date_format = date.strftime("%Y%m%d%H%M%S")
    new_archive = local(
        "tar -cvzf versions/web_static_{}.tgz web_static".format(date_format))
    if new_archive.succeeded:
        return "versions/web_static_{}.tgz web_static".format(date_format)
    else:
        return None
