#!/usr/bin/env python
# coding: utf-8

from .command import Command


class Help(Command):
    def run(self):
        doc = '''
bot help: botの説明
bot ping: pongを返す
bot todo: todoリストの管理
bot twitter: 指定した場所で投稿されたツイートを表示。詳しくはコマンド"bot twitter -h"で。
'''

        yield {
            'data': doc
        }

    @classmethod
    def command(cls):
        return 'help'
