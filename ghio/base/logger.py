from __future__ import print_function, unicode_literals

__author__ = "danishabdullah"

import logging

# create logger with 'spam_application'
LOG = logging.getLogger('ghio')
LOG.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the LOG
LOG.addHandler(ch)