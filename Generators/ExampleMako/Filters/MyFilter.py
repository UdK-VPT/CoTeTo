# a filter function is called with the following arguments:
#   d - the data dictionary read from the loader
#   systemCfg - system configuration
#   generatorCfg - generator configuration
#   logger - a logger instance


def myfilter(d, systemCfg, generatorCfg, logger):

    # spread a message
    logger.debug('Hi there! This is a filter running from module: ' + __file__)

    x = d['dummy']

    # manipulate some data
    x['foo'] += 1

    # add more data
    x['bar'] = 2.0 * x['foo']

    # no return needed - data is manipulated inplace
