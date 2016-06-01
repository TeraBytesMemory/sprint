#!/usr/bin/env python
# coding: utf-8

from .option import Option


class OptFloat(Option):
    def __init__(self, flag: str, default: str):
        float(default)
        super().__init__(flag, default)

    def parse(self, data: list):
        if self.flag in data:
            i = data.index(self.flag)
            try:
                result = float(data[i+1])
                new_data = data[:i] + data[i+2:]
            except (KeyError, ValueError):
                new_data = data[:i] + data[i+1:]
                result = float(self.default)
            return new_data, result
        else:
            return data, float(self.default)
