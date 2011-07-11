#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File: log_lines_manager.py
    Description: This module knows how to deal with log lines and prepares events
    to be sent.
"""


import re

from exception import *


class LogLinesManager:
    def __init__(self, conf):
        self.validate_conf(conf)
        self.conf = conf
        self.init_counts()
        self.consolidated = []
        self.event_queue = []

    def has_global_fields(self):
        return self.conf.has_key('global_fields')

    def init_counts(self):
        events_conf = self.conf['events_conf']
        for event_conf in events_conf:
            if event_conf.has_key('consolidation_conf'):                
                self.counts.update({event_conf['consolidation_conf']['field'] : 0})

    @staticmethod
    def validate_conf(conf):
        if not conf.has_key('log_filename'):
            raise LogFilenameNotFound()
        if not conf.has_key('events_conf'):
            raise EventsConfNotFound()
        for event_conf in conf['events_conf']:
            if not event_conf.has_key('eventtype'):
                raise EventtypeNotFound()
            if not event_conf.has_key('regexps'):   
                raise RegexpNotFound()

    def create_event(self, line, groups_matched, conf):
        event = {}
        event.update({'eventtype' : conf['eventtype']})
        event.update(groups_matched)
        if conf.has_key('one_event_per_line_conf') and \
           conf['one_event_per_line_conf'].has_key('user_defined_fields'):
            event.update(conf['one_event_per_line_conf']['user_defined_fields'])
            event.update({'line' : line})
        elif conf.has_key('consolidation_conf'):
            if conf['consolidation_conf'].has_key('enable') and \
                conf['consolidation_conf']['enable'] == False:
                pass
            else:
                self.counts[event_conf['consolidation_conf']['field']] += 1
        else:
            event.update({'line' : line})            
        if self.has_global_fields():
            event.update(self.conf['global_fields'])
        return event

    def process_line(self, line):
        events_conf = self.conf['events_conf']
        for event_conf in events_conf:
            regexps = event_conf['regexps']
            for regexp in regexps:
                match = re.match(regexp, line)
                if match:
                    event = self.create_event(line, match.groupdict(), event_conf)
                    self.event_queue.append(event)
                    return
