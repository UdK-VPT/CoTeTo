#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20190411 Joerg Raedler jraedler@udk-berlin.de
#
# This is an example of the usage of CoTeTo as a python module.
# 

import os
import sys

# check if we are running in the development folder -
# just a hack to run this script without installing CoTeTo first -
# usually not needed for users
parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if os.path.isfile(os.path.join(parent, 'setup.py')):
    sys.path.insert(0, parent)

#### Example Code 

# 1. import the controller class from CoTeTo
from CoTeTo.Controller import Controller

# 2. initialize a controller instance
# for a list of optional arguments see CoTeTo/Controller.py
con = Controller()

# 3. choose a generator ...
# a list of available generators can be printed with print(con.generators.keys())
gen = con.generators['Example01Mako::1.0']

# 4. ... and execute it!
# arguments are:
#   a list of input URIs (not used with the dummy loader)
#   a filename or prefix for the output
gen.execute(('spam', ), 'ModuleTestOutput.txt')
