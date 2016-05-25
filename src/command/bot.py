#!/usr/bin/env python
# coding: utf-8

from command import Command
from ping import Ping
from todo import Todo


class Bot(Command):

    def __init__(self, data):
        super().__init__(data)

        if not self.data[0] == self.__class__.command():
            return

        bot_command = data[1:]

        if bot_command[0] == Ping.command():
            self.command = Ping(bot_command)
        elif bot_command[0] == Todo.command():
            self.command = Todo(bot_command)

    def run(self):
        self.command.run()

    @classmethod
    def command(cls):
        return 'bot'
