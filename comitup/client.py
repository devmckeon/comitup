#!/usr/bin/python

#
# Copyright 2016-2017 David Steele <steele@debian.org>
# This file is part of comitup
# Available under the terms of the GNU General Public License version 2
# or later
#

import dbus
import sys

ciu_service = None

def get_method(fn_nm):
    global ciu_service

    if not ciu_service:
        bus = dbus.SystemBus()

        try:
            ciu_service = bus.get_object(
                           'com.github.davesteele.comitup',
                           '/com/github/davesteele/comitup'
                          )
        except dbus.exceptions.DBusException:
            print("Error connecting to the comitup D-Bus service")
            sys.exit(1)

    return ciu_service.get_dbus_method(fn_nm, 'com.github.davesteele.comitup')


def call_method(fn_name):
    def _call_method(fn):
        def wrapper(*args, **kwargs):
            return get_method(fn_name)(*args, **kwargs)

        return wrapper
    return _call_method


@call_method('state')
def ciu_points(*args, **kwargs):
    pass


@call_method('access_points')
def ciu_state(*args, **kwargs):
    pass


@call_method('delete_connection')
def ciu_delete(*args, **kwargs):
    pass


@call_method('connect')
def ciu_connect(*args, **kwargs):
    pass


@call_method('get_info')
def ciu_info(*args, **kwargs):
    pass
