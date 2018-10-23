#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 20170608 Joerg Raedler jraedler@udk-berlin.de
#
# XML file loader for CoTeTo
# 20180208 Werner Kaul we.kaul@udk-berlin.de'
#
from CoTeTo.Loader import Loader
from os.path import isfile

from lxml import etree, objectify
from urllib.request import urlopen
import re
from os import path

#convert xml to dict
def xml_to_dict(xml_object):
    if type(xml_object) not in [objectify.ObjectifiedElement, objectify.StringElement]:
        if type(xml_object) in [str, bytes]:
            xml_object = objectify.fromstring(xml_object)


    dict_object = {}

    #get the xsd

    #the namespace for each element can be found in nsmap with the prefix as key
    #if the prefix is None the element belongs to the basic namespace of the given xml-structure
    try:
            xmlns = xml_object.nsmap[xml_object.prefix]
    except:
        # If no basic namespace is defined the standard xml refers to "http://www.w3.org/XML/1998/namespace" as default.
        # It is not necessary to explicitly define it. So the basic namespace is set to an empty string
        xmlns = ''

    #lxml objectify deals with namespaces using the notation of James Clark
    #the namespace-string is stripped to simplify the handling of the resulting dict
    #(no loss of information as the namespace is already held in 'xmlns')
    tag = xml_object.tag
    if xmlns:
        try:
            tag = re.match('^\{'+xmlns+'\}(.*)$',tag).group(1)
        except:
            pass

    dict_object[tag] = {'base': xml_object.base,
                       'nsmap': xml_object.nsmap,
                       'prefix': xml_object.prefix,
                       'xmlns': xmlns,
                       'tail': xml_object.tail,
                       'text': xml_object.text,
                       'attrib': {}}

    for key in xml_object.attrib.keys():
        dict_object[tag]['attrib'][key] = xml_object.attrib[key]
    if type(xml_object) == objectify.ObjectifiedElement:
        dict_object[tag]['children'] = []
        for j in xml_object.getchildren():
            dict_object[tag]['children'].append(xml_to_dict(j))
    return dict_object

#validate xml against xsd-files in 'schema' or, if empty, against the schema information referenced by the xml structure
def xsd_collect(xml_object,schema = []):

    if type(xml_object) not in [objectify.ObjectifiedElement, objectify.StringElement]:
        if type(xml_object) in [str, bytes]:
            xml_object = objectify.fromstring(xml_object)

    for key in xml_object.attrib.keys():
        # get xsd references
        if key in (['schemaLocation', 'noNamespaceSchemaLocation'] +
                       ['{' + ns + '}schemaLocation' for ns in xml_object.nsmap.values()] +
                       ['{' + ns + '}noNamespaceSchemaLocation' for ns in xml_object.nsmap.values()]):
            # add to schema list
            if xml_object.attrib[key] not in schema:
                schema.append(xml_object.attrib[key])
    if type(xml_object) == objectify.ObjectifiedElement:
        for j in xml_object.getchildren():
            schema = xsd_collect(j, schema)
    return schema

def xsd_validate(xml_file,xsd_urilist=[]):

    #load xml-file

    xsd_locations =[]
    #get xsd_uris from xml if no xsd_uri ist given
    if xsd_urilist:
        xsd_locations = [['',a] for a in xsd_urilist]
    else:
        with open(xml_file, 'r') as f:
            xml = f.read().encode('utf8')
        for xsd in xsd_collect(xml):
            #get uri/xsd pairs
            tmp = xsd.split(" ")
            if len(tmp) == 1:
                # it's allowed to leave out the namespace uri if there is only one schema
                xsd_locations = xsd_locations+[('',tmp[0])]
            else:
                xsd_locations = xsd_locations+[list(tup) for tup in zip(tmp[0::2], tmp[1::2])]
    result = ''
    for xsd_loc in xsd_locations:
        # if there is no path information the xsd-file may be found where the xml-file resides
        if "/" not in xsd_loc[1]:
            xsd_loc[1] = "/".join(xml_file.split("/")[:-1])+"/"+xsd_loc[1]
        #check if schema file exists
        if not isfile(xsd_loc[1]):
            result = result + "Schema "+ xsd_loc[1] + ": File not found.\n"
        else:
            # validate the xml_file against the schema
            with open(xsd_loc[1], 'r') as f:
                xmlschema_doc = etree.parse(f)
                xmlschema = etree.XMLSchema(xmlschema_doc)
            with open(xml_file, 'r') as f:
                if not xmlschema.validate(etree.parse(f)):
                    result = result+ "Schema "+ xsd_loc[1]+ ": "+ str(xmlschema.error_log)+ "\n"
    return(result)

class XMLFile(Loader):
    name = 'XMLFile'
    description = 'XML file loader for CoTeTo'
    version = '1.0'
    author = 'Werner Kaul we.kaul@udk-berlin.de'
    helptxt = """Load XML files, validate them against xsd schemas (given or referenced by the xml structure), returns a hierarchic dict for each file"""



    def load(self, uriList):
        #get XML Schema File (
        xsd_urilist = list(filter(lambda uri: uri.endswith('.xsd'), uriList))
        # get XML-Files
        xml_urilist = filter(lambda uri: uri.endswith('.xml'), uriList)
        xml_dict = {}
        for xml_uri in xml_urilist:
            #validate xml against schema
            validation_error = xsd_validate(xml_uri, xsd_urilist)
            if validation_error:
                self.logger.info('XMLFile Validation Error: %s\n',validation_error)

            # open and read xml file
            with open(xml_uri, 'r') as f:
                    xml_dict[xml_uri] = xml_to_dict(f.read().encode('utf8'))

        return xml_dict
