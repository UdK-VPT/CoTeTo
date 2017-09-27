#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 201500225 Joerg Raedler jraedler@udk-berlin.de
#

import sys
import os
import os.path
import zipfile
import logging
import CoTeTo
from CoTeTo.Generator import Generator
from urllib.request import pathname2url


class Controller(object):

    """main controller of the code generation framework"""

    def __init__(self, generatorPath=[], logger='CoTeTo', logHandler=None, logLevel=logging.WARNING):
        # initialize logging system
        self.logger = logging.getLogger(logger)
        if logHandler is None:
            # fall back to stderr
            logHandler = logging.StreamHandler(sys.stderr)
        self.logger.addHandler(logHandler)
        self.logger.setLevel(logLevel)
        self.logger.info('Starting CoTeTo.Controller from file %s, version %s', __file__, CoTeTo.__version__)
        # create system configuration dict - will be available to subsystems
        self.systemCfg = {
            'platform': sys.platform,
            'version': CoTeTo.__version__,
            'path': os.path.dirname(os.path.realpath(__file__)),
            # need more here?
        }
        self.pathname2url = pathname2url
        # read standard loaders
        self.readStandardLoaders()
        # append a path from the parent folder - just for convenience
        parent = os.path.dirname(self.systemCfg['path'])
        p = os.path.join(parent, 'Generators')
        if os.path.isdir(p):
            generatorPath.append(p)
        # append a path from the parents parent folder - just for convenience
        parent = os.path.dirname(parent)
        p = os.path.join(parent, 'CoTeTo_Generators')
        if os.path.isdir(p):
            generatorPath.append(p)
        # still empty?
        if not generatorPath:
            raise Exception('No folders to search for generators specified!')
        self.generatorPath = generatorPath
        self.systemCfg['generatorPath'] = self.generatorPath
        # try to load available generators
        self.rescanGenerators()

    def readStandardLoaders(self):
        """read list of loaders and load corresponding modules"""
        import CoTeTo.Loaders
        import importlib
        self.loaders = {}
        self.logger.debug('CON-LDR | start loading')
        for l in CoTeTo.Loaders.__all__:
            self.logger.debug('CON-LDR | try to load: %s', l)
            m = importlib.import_module('.' + l, 'CoTeTo.Loaders')
            c = getattr(m, l)
            n = '%s::%s' % (c.name, c.version)
            self.loaders[n] = c

    def rescanGenerators(self):
        """rescan generatorPath and load generator packages"""
        self.generators = {}
        self.logger.debug('CON-GEN | start scan')
        for p in self.generatorPath:
            self.logger.debug('CON-GEN | scan path: %s', p)
            for e in os.listdir(p):
                o = os.path.join(p, e)
                if os.path.isdir(o) or zipfile.is_zipfile(o):
                    self.logger.debug('CON-GEN | load element: %s', o)
                    try:
                        g = Generator(self, o)
                        n = '%s::%s' % (g.name, g.version)
                        self.logger.debug('CON-GEN | found: %s::%s', g.name, g.version)
                        self.generators[n] = g
                    except Exception as e:
                        self.logger.exception('CON-GEN | exception while loading element')
