#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 201500225 Joerg Raedler jraedler@udk-berlin.de
#

import os, os.path, zipfile, tempfile, configparser

# mako template engine
from mako.template import Template
from mako.lookup import TemplateLookup
from mako.runtime import Context

# jinja2 template engine
from jinja2 import Environment, FileSystemLoader

from io import StringIO
import CoTeTo
from CoTeTo.import_file import import_file

# a template for the generator info text as txt and html
generatorInfoTmpl = {
'txt' : """
Name:        ${cfg['GENERATOR'].get('name')}
Description: ${cfg['GENERATOR'].get('description')}
Version:     ${cfg['GENERATOR'].get('version')}
Author:      ${cfg['GENERATOR'].get('author')}
Path:        ${path}

Data Loader:
    requires ${cfg['LOADER'].get('name')}, version ${cfg['LOADER'].get('minVer', '?')}...${cfg['LOADER'].get('maxVer', '?')}
    % if loader:
    using version ${loader.version}
    % else:
    *** NOT FOUND! ***
    % endif

Templates:
% for t in [s for s in cfg.sections() if s.upper().startswith('TEMPLATE')]:
    ${cfg[t].get('ext', 'DEFAULT')}: ${cfg[t].get('topFile')}
% endfor

% if cfg.has_section('PYFILTER'):
Python filter:
    ${cfg['PYFILTER'].get('module')}.${cfg['PYFILTER'].get('function')}
% endif
""",

'html' : """
<h2>${cfg['GENERATOR'].get('name')} - version ${cfg['GENERATOR'].get('version')}</h2>
<h3>Author</h3>
<p>${cfg['GENERATOR'].get('author')}</p>
<h3>Description</h3>
<p>${cfg['GENERATOR'].get('description')}</p>
<h3>Path</h3>
<p><a href="file:${p2u(path)}">${path}</a> </p>

<h3>Data Loader</h3>
<p>
Requires ${cfg['LOADER'].get('name')}, version ${cfg['LOADER'].get('minVer', '?')}...${cfg['LOADER'].get('maxVer', '?')}<br/>
% if loader:
Found <a href="loader://${loader.name}___${loader.version}">version ${loader.version}</a><br/>
% else:
<b>Not found, generator is not usable!</b><br/>
% endif
</p>

<h3>Templates</h3>
% for t in [s for s in cfg.sections() if s.upper().startswith('TEMPLATE')]:
<p><b>${cfg[t].get('ext', 'DEFAULT')}:</b> ${cfg[t].get('topFile')} </p>
% endfor

% if cfg.has_section('PYFILTER'):
<h3>Python filter</h3>
<p>${cfg['PYFILTER'].get('module')}.${cfg['PYFILTER'].get('function')}</p>
% endif
"""
}


class Generator(object):
    """represents a generator package """

    def __init__(self, controller, packagePath=None):
        self.controller = controller
        self.packagePath = packagePath
        self.tempDir = None
        self.logger = controller.logger
        self.logger.debug('GEN | start to create instance for path %s', packagePath)
        if zipfile.is_zipfile(packagePath):
            self.zf = zipfile.ZipFile(packagePath)
        else:
            self.zf = None
        self.cfg = configparser.ConfigParser()
        self.logger.debug('GEN | read Package.ini')
        self.cfg.read_file(self.getReadableFile('Package.inf'))
        g = self.cfg['GENERATOR']
        self.name = g.get('name')
        self.version = g.get('version')
        self.author = g.get('author')
        self.description = g.get('description')

        # check for a usable api
        lcfg = self.cfg['LOADER']
        self.loader = None
        self.logger.debug('GEN | locate loader')
        # FIXME: check for local loader class
        for loader in self.controller.loaders.values():
            if lcfg.get('name') == loader.name:
                if (lcfg.get('minVer', '000') <= loader.version) and (lcfg.get('maxVer', '999999') >= loader.version):
                    self.logger.debug('GEN | found loader: %s::%s', loader.name, loader.version)
                    self.loader = loader

    def infoText(self, fmt='txt'):
        """return information on this generator in text form"""
        t = Template(generatorInfoTmpl[fmt])
        return t.render(cfg=self.cfg, path=self.packagePath, loader=self.loader, p2u=self.controller.pathname2url)

    def getReadableFile(self, name, folder=''):
        """return a readable file-like object from package folder or zip"""
        if self.zf:
            f = self.zf.open(os.path.join(folder, name), 'r')
        else:
            f = open(os.path.join(self.packagePath, folder, name), 'r')
        return f

    def getTextFileContents(self, name, folder=''):
        """return a string read from a text file from package folder or zip"""
        if self.zf:
            s = str(self.zf.read(os.path.join(folder, name)), 'utf8')
        else:
            s = open(os.path.join(self.packagePath, folder, name), 'r').read()
        return s

    def getTemplateFolder(self):
        """return template folder, for zip packages extract to temporary folder first"""
        if not self.zf:
            return os.path.join(self.packagePath, 'Templates')
        if self.tempDir is None:
            self.tempDir = tempfile.TemporaryDirectory()
        tf = 'Templates/'
        tmpl = [f for f in self.zf.namelist() if f and f.startswith(tf) and f != tf]
        for t in tmpl:
            f = open(os.path.join(self.tempDir.name, os.path.split(t)[1]), 'wb')
            f.write(self.zf.read(t))
            f.close()
        return self.tempDir.name

    def executeLoader(self, uriList=[]):
        """execute the loader to fetch data from the source"""
        self.logger.debug('GEN | calling loader')
        l = self.loader(self.controller.systemCfg, self.cfg, self.logger)
        self.data = l(uriList)

    def executePyFilter(self):
        """execute the python filter to manipulate loaded data"""
        moduleName = self.cfg['PYFILTER'].get('module')
        functionName = self.cfg['PYFILTER'].get('function')
        modulePath = os.path.join(self.packagePath, 'Filters')
        self.logger.debug('GEN | import pyfilter module %s', moduleName)
        module = import_file(modulePath, moduleName)
        self.logger.debug('GEN | calling pyfilter function %s', functionName)
        function = getattr(module, functionName)
        function(self.data, self.controller.systemCfg, self.cfg, self.logger)

    def executeTemplates(self):
        """execeute all templates, return the output buffers and extensions"""
        tmpls = [s for s in self.cfg.sections() if s.upper().startswith('TEMPLATE')]
        txt = {}
        for tmpl in tmpls:
            ext = self.cfg[tmpl].get('ext', '')
            if ext in txt:
                while ext in txt:
                    ext.append('X')
                self.logger.error('GEN | file extension already exists, using %s!' % ext)
            self.logger.debug('GEN | processing template setup '+tmpl)
            txt[ext] = self.executeTemplate(tmpl)
        return txt

    def executeTemplate(self, name):
        """execeute a single template with the data, return the output buffer"""
        tmplType = self.cfg[name].get('type', 'mako')
        if tmplType == 'mako':
            self.logger.debug('GEN | calling mako template')
            tLookup = TemplateLookup(directories=[self.getTemplateFolder()])
            template = Template("""<%%include file="%s"/>""" %
                self.cfg[name].get('topFile'),
                lookup=tLookup, strict_undefined=True)
            buf = StringIO()
            ctx = Context(buf, d=self.data, systemCfg=self.controller.systemCfg,
                generatorCfg=self.cfg, logger=self.logger)
            template.render_context(ctx)
            buf.flush()
            buf.seek(0)
            return buf
        elif tmplType == 'jinja2':
            self.logger.debug('GEN | calling jinja2 template')
            env = Environment(loader=FileSystemLoader(self.getTemplateFolder()))
            template = env.get_template(self.cfg[name].get('topFile'))
            ns = {'d': self.data}
            ns['systemCfg'] = self.controller.systemCfg
            ns['generatorCfg'] = self.cfg
            ns['logger'] = self.logger
            tmp = template.render(ns)
            buf = StringIO(tmp)
            return(buf)
        else:
            raise Exception('Unknown template system: '+tmplType)

    def execute(self, uriList=[]):
        if not self.loader:
            raise Exception('Generator is not valid - canceling execution!')
        # fill data model from the loader using the data URIs
        self.executeLoader(uriList)
        # apply filter
        if self.cfg.has_section('PYFILTER'):
            self.executePyFilter()
        # handle data to template, return text buffer
        return self.executeTemplates()

    # make the generator executable
    __call__ = execute
