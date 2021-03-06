#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import gelfHandler

from schnueffelstueck import *

def parse_args():
  epilog = """
  SaltEventsGelf is a schnueffelstueck to schnueffel on salt events by attaching to the masters event bus.
  Events are formatted in GELF and sent to a logging host. Common end points are Graylog2 or logstash.
  """
  parser = argparse.ArgumentParser(description='SaltEventsGelf Schnueffelstueck', epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-lh', '--log_host', help='The host so send log messages to', dest='log_host', default='localhost')
  parser.add_argument('-lp', '--log_port', help='The port on the log host to send messages to', dest='log_port', default='12201')
  parser.add_argument('-lP', '--log_proto', help='The protocol to send messages over ("TCP", or "UDP" are currently supported)', dest='log_proto', default='TCP')
  parser.add_argument('--i_do_not_want_any_securtiy', help='If you do not want any security, set this switch', dest='no_tls', default=False, action='store_true')
  parser.add_argument('-s','--salt_sock_dir',  help='Staticly define the directory holding the salt unix sockets for communication', dest='salt_sock_dir', default='/var/run/salt')
  parser.add_argument('-n','--salt_node',  help='Staticly define the directory holding the salt unix sockets for communication', dest='salt_node', default='master',)
  parser.add_argument('-d', '--debug', help='additional debug output', dest='debug', default=False, action='store_true')

  return parser.parse_args()

def setup_logger(config):
    logger = logging.getLogger(__name__)
    if logger.handlers:
        logger.handlers = []
    if config.debug:
      print "initialising logger with: %s" % config
    logger.addHandler(gelfHandler.handler(host=config.log_host,
                                          port=config.log_port,
                                          proto=config.log_proto,
                                          tls=(not config.no_tls),
                                          facility='SaltEventGelf Schnueffelstueck'
                                          ))
    return logger

if __name__ == '__main__':
  config = parse_args()
  logger = setup_logger(config)
  schnueffelstueck = Schnueffelstueck(config, logger)
  schnueffelstueck.schnueffel()