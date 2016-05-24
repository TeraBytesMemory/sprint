#!/usr/bin/env python
# coding: utf-8

from command import Command
from model.todo import Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Todo(Command):

    def __init__(self, **args):
        super().__init__(**args)

        engine = create_engine('', echo=True)
        self.session = sessionmaker(bind=engine)

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
        context = ' '.join(self.data[4:])

        new_colum = Todo(name=name,
                         context=context)

        self.session.add(new_colum)
        self.session.commit()

        return {
            "data": "todo added"
        }

    def delete(self):
        name = self.data[3]

        self.session.query(
            Todo
        ).filter(
            Todo.name == name
        ).delete()

        return {
            "data": "todo deleted"
        }

    def list(self):
        items = self.session.query(Todo).all()

        result = '\n'.join(items)

        return {
            "data": result
        }
