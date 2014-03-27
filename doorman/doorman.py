#!/usr/bin/env python2.7

"""Doorman daemon. Spawns a process that manages the latch."""
import logging
import daemon # must be python-daemon, not daemon

from actuator import Latch
from attempts import EntryAttemptInterface
from recognizer import Recognizer

# TODO: Add options for the interval and for the location of the db and log files, and
# maybe try to read them from /etc/latchburg.conf or something like that

INTERVAL = 10 # seconds to hold latch open

def guard():
  """Function to continually accept input and determine when to unlock door."""

  # TODO: How can we verify that this is running? Should it periodically call home?

  LOGFORMAT = '%(asctime)-15s %(message)s'
  logging.basicConfig(filename='latchburg.log', level=logging.DEBUG, format=LOGFORMAT)

  ver = Recognizer()
  interface = EntryAttemptInterface()
  latch = Latch()

  while True:
    attempt = interface.getAttempt()
    if attempt == None:
      break

    if ver.check(attempt):
      latch.unlock(INTERVAL)
      logging.info('Allowed access for attempt: %s', attempt)
    else:
      logging.warning('Unauthorized attempt: %s', attempt)


def main():
  """Daemonize"""
  with daemon.DaemonContext():
    guard()


if __name__ == "__main__":
  main()
