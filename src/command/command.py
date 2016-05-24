#!/usr/bin/env python
# coding: utf-8

from abc import ABCmeta, abstractmethod


class Command(metaclass=ABCmeta):

    def __init__(self, data):
        self.data = data.split()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    @classmethod
    def command(cls):
        pass
