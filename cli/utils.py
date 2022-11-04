import os
import sys


def current_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def is_addon_dir(path=None):
    if not path:
        path = current_dir()
    # TODO: Check if this is a valid requirement for confirming an addon dir
    return os.path.exists(os.path.join(path, "__init__.py"))