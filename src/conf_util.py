#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    File: conf_util.py 
    Description: This module gather util functions for log confs.
"""

from exception import *


def validate_conf(conf):
    if not conf.has_key('log_filename'):
        raise LogFilenameNotFound(conf)

    if not conf.has_key('events_conf'):
        raise EventsConfNotFound(conf)

    for event_conf in conf['events_conf']:
        if not event_conf.has_key('eventtype'):
            raise EventtypeNotFound(event_conf)

        if not event_conf.has_key('regexps'):
            raise RegexpNotFound(event_conf)


def is_consolidation_enabled(event_conf):
    return (event_conf.has_key('consolidation_conf') and not \
            event_conf['consolidation_conf'].has_key('enable')) or \
           (event_conf.has_key('consolidation_conf') and \
            event_conf['consolidation_conf'].has_key('enable') and \
            event_conf['consolidation_conf']['enable'] == True)


def has_global_fields(conf):
    return conf.has_key('global_fields')
