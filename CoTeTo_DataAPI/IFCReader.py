#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170123 Christoph Nytsch-Geusen nytsch@udk-berlin.de
#

name = 'IFCReader'
description = 'IFC file reader, return ifcOpenShell object from IFC files'
version = '0.1'
author = 'Christoph Nytsch-Geusen'
helptxt = """
..."""

def fetchData(uriList, systemCfg, generatorCfg, logger):
    from os.path import isfile
    import ifcopenshell
    ifcf = {}
    if not uriList:
        logger.critical('IFCReader - no files specified!')
        raise Exception('No files specified!')
    for f in uriList:
        if isfile(f):
            logger.info('IFCReader - loading %s', f)
            ifcf[f] = ifcopenshell.open(str(f))
        else:
            ifcf[f] = None
            logger.error('IFCReader - file not readable %s', f)
    return {'ifc_files': ifcf}
