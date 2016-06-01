#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    context = Column(String)

    def __init__(self, name: str, context: str):
        self.name = name
        self.context = context
