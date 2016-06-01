#!/usr/bin/env python
# coding: utf-8

from .command import Command
from .ping import Ping
from .todo import Todo
from .twitter import Twitter


class Bot(Command):

    def __init__(self, data):
        super().__init__(data)

        bot_command = self.data[1:]

        if bot_command[0] == Ping.command():
            self.command = Ping(bot_command)
        elif bot_command[0] == Todo.command():
            self.command = Todo(bot_command)
        elif bot_command[0] == Twitter.command():
            self.command = Twitter(bot_command)

    def run(self):
        yield {
            "data": ' '.join(self.data)
        }
        yield from self.command.run()

    @classmethod
    def command(cls):
        return 'bot'
