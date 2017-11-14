#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#
from CoTeTo.Loader import Loader
from os.path import isfile
from json import load


class JSONFile(Loader):
    name = 'JSONFile'
    description = 'JSON file loader for CoTeTo'
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """Load JSON files, returns a dictionary for each file"""

    def load(self, uriList):
        data = {}
        for u in uriList:
            if isfile(u):
                self.logger.info('JSONFile - loading %s', u)
                data[u] = load(open(u, 'r'))
            else:
                data[u] = None
                self.logger.error('JSONFile - file not readable %s', u)
        return data
