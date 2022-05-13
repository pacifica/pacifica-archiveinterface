#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module to convert an integer id to a filepath for storage system.

Mathematically, this is a bijective_ set of methods. This means that
running `filename2id(id2filename(ID))` must return the same `ID`
passed and conversely `id2filename(filename2id(PATH))` must return
the same `PATH` passed.

Example usage:

::

  >>> id2filename(1234)
  '/d2/4d2'
  >>> filename2id('/d2/4d2')
  1234

.. _bijective: https://en.wikipedia.org/wiki/Bijection
"""
from __future__ import print_function
import sys


def id2filename(fileid):
    """Algorithm for getting filepath from an integer id."""
    hexfileid = "{0:x}".format(fileid)
    directories = ""
    while len(hexfileid) > 2:
        directories = "{0}/{1}".format(directories, hexfileid[-2:])
        hexfileid = hexfileid[:-2]
    if directories == "":
        filename = "file.{0}".format(hexfileid)
        filepath = "/{0}".format(filename)
        directories = "/"
    else:
        filename = "{0:x}".format(fileid)
        filepath = "{0}/{1}".format(directories, filename)
    return filepath


def filename2id(path):
    """Convert a filepath to and ID."""
    if path[:6] == "/file.":
        return int(path[6:], 16)
    return int(path.split("/")[-1], 16)


if __name__ == "__main__":  # pragma: no cover
    print(id2filename(int(sys.argv[1])))
