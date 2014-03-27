#!/usr/bin/env python2.7

"""Doorman daemon. Spawns a process that manages the latch."""
import logging
import daemon

import actuator as actuator
from attempts import EntryAttemptInterface
from recognizer import Recognizer

INTERVAL = 10 # seconds to hold latch open

def guard():
  """Function to continually accept input and determine when to unlock door."""

  LOGFORMAT = '%(asctime)-15s %(message)s'
  logging.basicConfig(filename='latchburg.log', level=logging.DEBUG, format=LOGFORMAT)

  ver = Recognizer()
  interface = EntryAttemptInterface()

  while True:
    attempt = interface.getAttempt()
    if attempt == None:
      break

    if ver.check(attempt):
      actuator.unlock(INTERVAL)
      logging.info('Allowed access for attempt: %s', attempt)
    else:
      logging.warning('Unauthorized attempt: %s', attempt)


def main():
  """Daemonize"""
  with daemon.DaemonContext():
    guard()


if __name__ == "__main__":
  main()
