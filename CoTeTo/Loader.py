#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#

class Loader(object):
    """base class for a data loader in CoTeTo"""

    def __init__(self, systemCfg, generatorCfg, logger):
        self.systemCfg = systemCfg
        self.generatorCfg = generatorCfg
        self.logger = logger
        self.logger.debug('LDR | creating instance of loader')
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
        try:
            self.load(uriList)
        except:
            self.logger.exception('LDR | error during execution/load')

    # make class callable
    __exec__ = execute
