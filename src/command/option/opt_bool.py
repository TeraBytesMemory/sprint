#!/usr/bin/env python
# coding: utf-8

from .option import Option


class OptBool(Option):
    def __init__(self, flag: str):
        super().__init__(flag, 'False')

    def parse(self, data: list):
        if self.flag in data:
            i = data.index(self.flag)
            new_data = data[:i] + data[i+1:]

            return new_data, True
        else:
            return data, False
