#
#  The following objects can be used in templates: 
#
#  systemCfg - dictionary with information on the system and the environment
#    Keys:          ${' '.join(systemCfg.keys())}
#    CoTeToVersion: ${systemCfg['version']}
#    CoTeToPath:    ${systemCfg['path']}
#    Platform:      ${systemCfg['platform']}
#    FullPlatform:  ${systemCfg['fullplatform']}
#    Hostname:      ${systemCfg['hostname']}
#    Username:      ${systemCfg['username']}
#    GeneratorPath: ${', '.join(systemCfg['generatorPath'])}
#
#    the following are functions and need to be executed: 
#    Timestamp:     ${systemCfg['timestamp']()}
#    Infostamp:     ${systemCfg['infostamp']()}
#
#  generatorCfg - configparser object with information on the used generator
#    (this is basically the contents of the Package.inf file)
#    Sections:      ${' '.join(generatorCfg.keys())}
#    Name:          ${generatorCfg['GENERATOR'].get('name')}
#    Version:       ${generatorCfg['GENERATOR'].get('version')}
#
#    access to custom sections and values is also possible:
#    Answer:        ${generatorCfg['MYCUSTOMSETTINGS'].getint('answer')}
#
#  logger - an object to send logging messages
#    this will output None, but log a message: ${logger.info('The answer is 42!')}
#    suppress the output with this trick: ${logger.warning('But what was the question?') or ''}
#
#  d - the data object read from the loader and (optionally) manipulated by the filter
#    (this is usually a dictionary of the form filename : data_items, 
#     but this depends on the loader and filter code)  
#    Keys (Filenames/URIs):    ${' '.join(d.keys())}

The value of foo is ${d['dummy']['foo']}. Please notice this value was manipulated by a filter function.

## Templates can be splitted and included:
<%include file="Sub.mako"/>