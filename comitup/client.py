#!/usr/bin/python

#
# Copyright 2016-2017 David Steele <steele@debian.org>
# This file is part of comitup
# Available under the terms of the GNU General Public License version 2
# or later
#

import dbus
import sys
from functools import wraps


ciu_service = None
ciu_fns = {}


def ciu_decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global ciu_service
        global ciu_fns

        if ciu_service is None:
            try:
                bus = dbus.SystemBus()
                ciu_service = bus.get_object(
                               'com.github.davesteele.comitup',
                               '/com/github/davesteele/comitup'
                              )
            except dbus.exceptions.DBusException:
                print("Error connecting to the comitup D-Bus service")
                sys.exit(1)

        fn_name = fn.__name__[4:]
        if fn_name not in ciu_fns:
            ciu_fns[fn_name] = ciu_service.get_dbus_method(
                fn_name,
                'com.github.davesteele.comitup',
            )

        return ciu_fns[fn_name](*args, **kwargs)

    return wrapper


@ciu_decorator
def ciu_state(*args, **kwargs):
    pass


@ciu_decorator
def ciu_points(*args, **kwargs):
    pass


@ciu_decorator
def ciu_delete(*args, **kwargs):
    pass


@ciu_decorator
def ciu_connect(*args, **kwargs):
    pass


@ciu_decorator
def ciu_info(*args, **kwargs):
    pass
