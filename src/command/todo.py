#!/usr/bin/env python
# coding: utf-8

from command import Command
from model.todo import Todo as TodoModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Todo(Command):

    def __init__(self, **args):
        super().__init__(**args)

        engine = create_engine('', echo=True)
        self.session = sessionmaker(bind=engine)

    def run(self):
        todo_command = self.data[1]
        name = self.data[2]
        context = self.data[3:]

        if todo_command == 'add':
            return self.add(name, context)
        elif todo_command == 'delete':
            return self.delete(name)
        elif todo_command == 'list':
            return self.list()

    @classmethod
    def command(cls):
        return "todo"

    def add(self, name, context):
        new_colum = TodoModel(name=name,
                              context=context)

        self.session.add(new_colum)
        self.session.commit()

        return {
            "data": "todo added"
        }

    def delete(self, name):
        self.session.query(
            TodoModel
        ).filter(
            TodoModel.name == name
        ).delete()

        return {
            "data": "todo deleted"
        }

    def list(self):
        items = self.session.query(TodoModel).all()

        result = '\n'.join(items)

        return {
            "data": result
        }
