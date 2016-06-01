#!/usr/bin/env python
# coding: utf-8

from .command import Command
from model.todo import Todo as TodoModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Todo(Command):

    def __init__(self, data):
        super().__init__(data)

        db_url = 'postgres://npvztuassmpeql:NijXOxZWRtvgL5eGQUz1olMTzP@ec2-23-23-95-27.compute-1.amazonaws.com:5432/d6buclujgtf4c6'

        engine = create_engine(db_url, echo=True)
        Session = sessionmaker(bind=engine)

        self.session = Session()

    def run(self):
        todo_command = self.data[1]

        if todo_command == 'add':
            yield self.add(self.data[2], self.data[3:])
        elif todo_command == 'delete':
            yield self.delete(self.data[2])
        elif todo_command == 'list':
            yield self.list()

    @classmethod
    def command(cls):
        return "todo"

    def add(self, name, context):
        context = ' '.join(context)
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
        self.session.commit()

        return {
            "data": "todo deleted"
        }

    def list(self):
        items = self.session.query(TodoModel).all()
        items = ['{0} {1}'.format(i.name, i.context)
                 for i in items]
        if len(items) > 0:
            result = '\n'.join(items)
        else:
            result = 'todo empty'
        return {
            "data": result
        }
