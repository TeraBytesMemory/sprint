#!/usr/bin/env python
# coding: utf-8

from model.todo import Base
from sqlalchemy import create_engine

if __name__ == '__main__':
    db_url = 'postgresql://yterazawa@localhost:5432/todo'

    engine = create_engine(db_url, echo=True)

    Base.metadata.create_all(engine)
