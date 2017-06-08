#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#

class Loader(object):
    name = 'Loader'
    description = 'Abstract loader class for CoTeTo - should not be used directly.'
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """This is just an abstract class, real loaders should reimplement setup() and load()"""


    def __init__(self, systemCfg, generatorCfg, logger):
        self.systemCfg = systemCfg
        self.generatorCfg = generatorCfg
        self.logger = logger
        self.logger.debug('LDR | creating instance of loader %s' % self.name)
        try:
            self.setup()
        except:
            self.logger.exception('LDR | error during setup')
            
   
    def setup(self):
        """generic setup method - should be overwritten in loaders implementation"""
        self.logger.debug('LDR | empty generic setup method called')

    
    def load(self, uriList):
        """generic setup method - should be overwritten in loaders implementation"""
        self.logger.debug('LDR | empty generic load method called')


    def execute(self, uriList):
        self.logger.debug('LDR | executing loader %s with uriList: %s' % (self.name, uriList))
        try:
            return self.load(uriList)
        except:
            self.logger.exception('LDR | error during execution/load')

    # make class callable
    __exec__ = execute
