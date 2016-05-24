#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import String, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    name = Column(String)
    context = Column(String)

    def __init__(self, name: str, context: str):
        self.name = name
        self.context = context
