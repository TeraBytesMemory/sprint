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

    @abstractmethod
    def run(self):
        pass

    @classmethod
    @abstractmethod
    def command(cls):
        pass
