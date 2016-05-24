#!/usr/bin/env python
# coding: utf-8

from abc import ABCmeta, abstractmethod


class Command(metaclass=ABCmeta):

    def __init__(self, data: list):
        self.data = data

        if self.data[1] != self.__class__.command():
            raise TypeError

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    @classmethod
    def command(cls):
        pass
