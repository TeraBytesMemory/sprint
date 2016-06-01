#!/usr/bin/env python
# coding: utf-8

from .opt_bool import OptBool
from .opt_float import OptFloat


class OptionParser(object):

    def __init__(self):
        self.options = []

    def add_option(self, flag: str, _type: type, default: str = ''):
        if _type == float:
            op = OptFloat(flag, default)
            self.options.append(op)
        elif _type == bool:
            op = OptBool(flag)
            self.options.append(op)
        else:
            raise TypeError

    def parse(self, data: list):
        result = {}
        new_data = data

        for op in self.options:
            new_data, value = op.parse(new_data)
            result[op.flag] = value

        return new_data, result
