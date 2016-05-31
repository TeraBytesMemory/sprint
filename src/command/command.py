#!/usr/bin/env python
# coding: utf-8

from abc import ABCMeta, abstractmethod
import re


class Command(metaclass=ABCMeta):

    def __init__(self, data):
        if type(data) == list:
            self.data = data
        elif type(data) == str:
            self.data = data.split(' ')

        if self.data[0] != self.__class__.command():
            raise TypeError

        self.flag = {}
        self.long_flag
        self.default = {}

    def _add_flag(self, flag: str, _type: type, default: str, _long=None):
        if not re.match(r'-\w', flag):
            raise ValueError
        if flag[:1] == '--':
            _long = flag

        self.flag[flag] = {
            'type': _type,
            'default': default
        }

        self.default[flag] = default
        if type(_long) == str:
            if flag[:1] != '--':
                raise ValueError

            self.long_flag = {
                'type': _type,
                'default': default,
                'short': flag
            }

    def _run_flag(self) -> dict:
        result = {}

        for k, v in self.flag:
            if k in self.data:
                try:
                    i = self.data.index(k)
                    value = self.data[i+1]
                    if not (re.match(r'-\w', value) \
                            or value[:1] == '--'):
                        result[k] = type(value)
                except (IndexError, ValueError):
                    continue

        return result

    @abstractmethod
    def run(self):
        pass

    @classmethod
    @abstractmethod
    def command(cls):
        pass
