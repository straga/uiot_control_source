# MicroPython uasyncio module
# MIT license; Copyright (c) 2019 Damien P. George

from .core import *

from .funcs import wait_for
from .funcs import gather
from .event import Event
from .lock import Lock
from .stream import open_connection
from .stream import start_server
from .queues import Queue

# __version__ = (3, 0, 0)
#
# _attrs = {
#     "wait_for": "funcs",
#     "gather": "funcs",
#     "Event": "event",
#     "Lock": "lock",
#     "open_connection": "stream",
#     "start_server": "stream",
# }
#
# # Lazy loader, effectively does:
# #   global attr
# #   from .mod import attr
# def __getattr__(attr):
#     mod = _attrs.get(attr, None)
#     if mod is None:
#         raise AttributeError(attr)
#     value = getattr(__import__(mod, None, None, True, 1), attr)
#     globals()[attr] = value
#     return value
