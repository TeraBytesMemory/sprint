#!/usr/bin/env python
# coding: utf-8

from command import Command


class Ping(Command):

    def run(self):
        return {
            "data": "pong"
        }

    @classmethod
    def command(cls):
        return "ping"
