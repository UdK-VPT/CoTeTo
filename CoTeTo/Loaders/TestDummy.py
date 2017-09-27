#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#
from CoTeTo.Loader import Loader
from os.path import isfile

class TestDummy(Loader):
    name = 'TestDummy'
    description = "'Test loader that returns some data - doesn't need any input"
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """just return some meaningless data"""

    def load(self, uriList):
        data = {}
        d = {}
        d['foo'] = 42
        d['spam'] = "I'm a placeholder"
        d['eggs'] = list(range(100))
        d['weekdays'] = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        d['nonsense'] = {0: 'x', 'y': 1, 'abc':{'def':'ghi'}}
        data['dummy'] = d
        return data
