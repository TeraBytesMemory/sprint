#!/usr/bin/env python
# coding: utf-8

from abc import ABCMeta, abstractmethod
import re
from .option.option_parser import OptionParser


class Command(metaclass=ABCMeta):

    def __init__(self, data):
        if type(data) == list:
            self.data = data
        elif type(data) == str:
            self.data = data.split(' ')

        if self.data[0] != self.__class__.command():
            raise TypeError

        self.opt_parser = OptionParser()

    def _add_option(self, flag: str, _type: type, default: str = ''):
        self.opt_parser.add_option(flag, _type, default)

    def _parse_option(self):
        new_data, result = self.opt_parser.parse(self.data)
        self.data = new_data
        return result

    @abstractmethod
    def run(self):
        pass

    @classmethod
    @abstractmethod
    def command(cls):
        pass
