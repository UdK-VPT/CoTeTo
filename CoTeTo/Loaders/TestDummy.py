#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#
from CoTeTo.Loader import Loader
from os.path import isfile

class TestDummy(Loader):
    name = 'TestDummy'
    description = 'Test dummy that returns some data'
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """just return some meaningless data"""

    def load(self, uriList):
        data = {}
        data['foo'] = 42
        data['data'] = 'Im a placeholder!'
        return data
