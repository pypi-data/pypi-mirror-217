from __future__ import absolute_import

__version__ = "3.4.0"


def get_instance():
    from . import instance

    return instance.instance
