#!/usr/bin/env python

import sys

lb = [('>>> Checking dependencies for CoTeTo <<<',)]


def done(status=0):
    """write linebuffer lb and exit with status"""
    for l in lb:
        print(' '.join(l))
    # wait for a keypress to keep terminal open on Windows
    print('>>> Press ENTER to continue! <<<')
    sys.stdin.read(1)
    sys.exit(status)


# Checking platform
p = sys.platform
l = ['Checking platform... ', p]
if p in ('linux', 'linux2', 'win32'):
    l.append('- Ok!')
else:
    l.append('- Unsupported - good luck!')
lb.append(l)

# Checking python version
py35 = False
v = sys.version_info
l = ['Checking python version... ', '.'.join(str(i) for i in v)]
if v >= (3, 5):
    py35 = True
    l.append('- Ok!')
else:
    l.append('- Please install Python 3.5 or newer and retry!')
    lb.append(l)
    done(1)
lb.append(l)

# Checking Mako
l = ['Checking mako template engine... ']
try:
    from mako.template import Template
    l.append('Ok!')
except BaseException:
    l.append('- Please install mako and retry (pip install mako)!')
lb.append(l)

# Checking Jinja2
l = ['Checking jinja2 template engine... ']
try:
    from jinja2 import Environment
    l.append('Ok!')
except BaseException:
    l.append('- Please install jinja2 and retry (pip install jinja2)!')
lb.append(l)

# Checking PyQt5
l = ['Checking PyQt5... ']
try:
    from PyQt5 import QtGui
    l.append('Ok!')
except BaseException:
    l.append('- GUI will not run, please install PyQt5 and retry!')
lb.append(l)

done(0)
