#!/usr/bin/env python
# coding: utf-8

from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):

    def __init__(self, data):
        if type(data) == list:
            self.data = data
        elif type(data) == str:
            self.data = data.split(' ')

        if self.data[0] != self.__class__.command():
            raise TypeError

        self.flag = {}
        self.default = {}

    def _add_flag(self, callback, flag: str, default: str, full=None):
        if flag[0] != '-':
            raise ValueError
        if flag[:1] == '--':
            full = flag

        self.flag[flag] = {
            'callback': callback,
            'default': default
        }
        self.default[flag] = default
        if type(full) == str:
            if flag[:1] != '--':
                raise ValueError

            self.flag[full] = {
                'callback': callback,
                'default': default
            }

    def _run_flag(self):
        for k, v in self.flag:
            if k in self.data:
                i = self.data.index(k)
                if i + 1 == len(self.data):
                    v['callback'](v['default'])


    @abstractmethod
    def run(self):
        pass

    @classmethod
    @abstractmethod
    def command(cls):
        pass
