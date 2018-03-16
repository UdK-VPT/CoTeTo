#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#

from string import Template
from urllib.request import pathname2url

# a template for the loader info text as txt and html
loaderInfoTmpl = {
    'txt': """
Name:        ${name}
Description: ${description}
Version:     ${version}
Author:      ${author}
Path:        ${filename}
""",
    'html': """
<h2>${name} - version ${version}</h2>
<h3>Author</h3>
<p>${author}</p>
<h3>Description</h3>
<p>${description}</p>
<h3>Path</h3>
<p><a href="file:${fileurl}">${filename}</a></p>

<h3>Help</h3>
<p>${helptxt}</p>
"""
}


class Loader(object):
    name = 'Loader'
    description = 'Abstract loader class for CoTeTo - should not be used directly.'
    version = '1.0'
    author = 'Joerg Raedler jraedler@udk-berlin.de'
    helptxt = """This is just an abstract class, real loaders should reimplement setup() and load()"""
    isCustom = False
    isSetUp = False

    def __init__(self, systemCfg, generatorCfg, logger):
        self.systemCfg = systemCfg
        self.generatorCfg = generatorCfg
        self.logger = logger
        self.logger.debug('LDR | creating instance of loader %s' % self.name)
        try:
            self.setup()
            self.isSetUp = True
        except BaseException:
            self.logger.exception('LDR | error during setup')
            self.isSetUp = False

    def setup(self):
        """generic setup method - should be overwritten in loaders implementation"""
        self.logger.debug('LDR | empty generic setup method called')

    def load(self, uriList):
        """generic setup method - should be overwritten in loaders implementation"""
        self.logger.debug('LDR | empty generic load method called')

    def execute(self, uriList):
        self.logger.debug('LDR | executing loader %s with uriList: %s' % (self.name, uriList))
        if not self.isSetUp:
            raise Exception('LDR | loader was not successfully set up - will not execute!')
            return None
        try:
            return self.load(uriList)
        except BaseException:
            self.logger.exception('LDR | error during execution/load')

    # make class callable
    __call__ = execute

    def infoText(self, fmt='txt'):
        """return information on this loader in text form"""
        t = Template(loaderInfoTmpl[fmt])
        return t.substitute(name=self.name, description=self.description, author=self.author, version=self.version,
                            helptxt=self.helptxt, filename=__file__, fileurl=pathname2url(__file__))
