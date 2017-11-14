#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#
from CoTeTo.Loader import Loader
from os.path import isfile

class MyLoader(Loader):
    name = 'MyLoader'
    description = 'custom loader for custom files'
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """Load custom files, returns a dictionary for each file.
    The files contain `key : value` pairs, one per line."""

    def load(self, uriList):
        data = {}
        for u in uriList:
            if isfile(u):
                self.logger.info('MyLoader - loading %s', u)
                with open(u, 'r') as f:
                    d = {}
                    for l in f:
                        if l:
                            e = l.split(':')
                            if len(e) > 1:
                                d[e[0].strip()] = ':'.join(e[1:]).strip()
                    data[u] = d
            else:
                data[u] = None
                self.logger.error('MyLoader - file not readable %s', u)
        return data
