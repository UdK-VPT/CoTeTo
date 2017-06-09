#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#
from CoTeTo.Loader import Loader
from os.path import isfile

class TextFile(Loader):
    name = 'TextFile'
    description = 'Text file loader for CoTeTo'
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """Load text files, returns an list of lines for each file"""
    
    def load(self, uriList):
        data = {}
        for u in uriList:
            if isfile(u):
                self.logger.info('TextFile - loading %s', u)
                with open(u, 'r') as f:
                    data[u] = f.readlines()
            else:
                data[u] = None
                self.logger.error('TextFile - file not readable %s', u)
        return data
