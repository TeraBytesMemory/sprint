#!/usr/bin/env python
# coding: utf-8

import re
from abc import ABCMeta, abstractmethod


class Option(metaclass=ABCMeta):
    def __init__(self, flag: str, default: str):
        self.flag_list = []

        if self.isFlag(flag):
            self.flag = flag
            self.default = default
        else:
            raise ValueError

    @abstractmethod
    def parse(self, data):
        pass

    def isFlag(self, flag):
        return bool(re.match(r'-\w', flag) or re.match(r'--\w+', flag))
