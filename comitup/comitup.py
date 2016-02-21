#!/usr/bin/python


import logging
from logging.handlers import TimedRotatingFileHandler
import persist
import config
import random

import gobject
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

import statemgr

PERSIST_PATH = "/var/lib/comitup/comitup.json"
CONF_PATH = "/etc/comitup.conf"
LOG_PATH = "/var/log/comitup.log"


def deflog():
    log = logging.getLogger('comitup')
    log.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(
                LOG_PATH,
                encoding='utf=8',
                when='D',
                interval=7,
                backupCount=8,
              )
    fmtr = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
           )
    handler.setFormatter(fmtr)
    log.addHandler(handler)

    return log


def load_data():
    conf = config.Config(
                CONF_PATH,
                defaults = {
                    'base_name': 'comitup',
                    'web_port': '8080',
                },
             )

    data = persist.persist(
                PERSIST_PATH,
                {'id': str(random.randrange(1000, 9999))},
           )

    return (conf, data)


def inst_name(conf, data):
    return conf.base_name + '-' + data.id


def main():
    log = deflog()
    log.info("Starting comitup")

    (conf, data) = load_data()

    statemgr.init_state_mgr(
                inst_name(conf, data) + '.local',
                conf.base_name + '.local'
             )

    loop = gobject.MainLoop()
    loop.run()


if __name__ == '__main__':
    main()
