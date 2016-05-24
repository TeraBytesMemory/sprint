#!/usr/bin/env python
# coding: utf-8

from command.ping import Ping
from command.todo import Todo


class Bot(object):

    def __init__(self, data):
        self.data = data.split()

        if not self.data[0] == 'bot':
            return

        if self.data[1] == 'ping':
            self.command = Ping(data)
        elif self.data[1] == 'todo':
            self.command = Todo(data)

    def run(self):
        self.command.run()
