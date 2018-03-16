#
#   CoTeTo
#       Version:  ${systemCfg['version']}
#       Platform: ${systemCfg['platform']}
#       Path:     ${systemCfg['path']}
#       Gen-Path: ${', '.join(systemCfg['generatorPath'])}
#
#   Generator
#       Name:     ${generatorCfg['GENERATOR'].get('name')}
#       Version:  ${generatorCfg['GENERATOR'].get('version')}

The value of foo is ${d['dummy']['foo']}.

<%include file="Sub.mako"/>
