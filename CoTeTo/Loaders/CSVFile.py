#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#
from CoTeTo.Loader import Loader
from os.path import isfile
from csv import Sniffer, DictReader


class CSVFile(Loader):
    name = 'CSVFile'
    description = 'CSV file loader for CoTeTo'
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """Load CSV files, returns a csv.DictReader instance for each file"""

    def load(self, uriList):
        data = {}
        for u in uriList:
            if isfile(u):
                self.logger.info('CSVFile - loading %s', u)
                with open(u, r) as f:
                    dialect = Sniffer().sniff(f.read(1024))
                    f.seek(0)
                    data[u] = DictReader(f, dialect)
            else:
                data[u] = None
                self.logger.error('CSVFile - file not readable %s', u)
        return data
