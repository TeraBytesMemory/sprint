#!/usr/bin/env python
# coding: utf-8

from command import Command
from run_query import run_query


class Todo(Command):

    def run(self):
        todo_command = self.data[2]

        if todo_command == 'add':
            return self.add()
        elif todo_command == 'delete':
            return self.delete()
        elif todo_command == 'list':
            return self.list()

    @classmethod
    def command(cls):
        return "todo"

    def add(self):
        name = self.data[3]
        context = self.data[4]

        try:
            self.run_query(
                "INSERT INTO todo (name context) VALUE ('{0}' '{1}')"
                .format(name, context))

            return {
                "data": "todo added"
            }
        except:
            return {
                "error": "error"
            }

    def delete(self):
        name = self.data[3]

        try:
            self.run_query(
                "DELETE FROM todo WHERE name = '{}'"
                .format(name))

            return {
                "data": "todo deleted"
            }
        except:
            return {
                "error": "error"
            }

    def list(self):
        pass

    def init_db(self):
        self.run_query("CREATE TABLE todo (id serial PRIMARY KEY, name varchar, context varchar);")
