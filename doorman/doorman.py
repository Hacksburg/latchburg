#!/usr/bin/env python2.7

"""Doorman daemon. Spawns a process that manages the latch."""
import daemon # must be python-daemon, not daemon
import lockfile
import logging

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
  logging.basicConfig(filename='/var/log/latchburg.log', level=logging.DEBUG, format=LOGFORMAT)

  ver = Recognizer()
  interface = EntryAttemptInterface()
  latch = Latch()

  while True:
    try:
      attempt = interface.getAttempt()
      if attempt == None:
        break

      result = ver.check(attempt)
      if result != None:
        latch.unlock(INTERVAL)
        logging.info('Allowed access for attempt with digest %s', result)
      else:
        logging.warning('Unauthorized attempt: %s', attempt)
    except Exception as inst:
      logging.error(inst)


def main():
  """Daemonize"""
  context = daemon.DaemonContext(
      working_directory='/var/lib/latchburg',
      pidfile=lockfile.FileLock('/var/run/latchburg.pid')
      )

  #TODO: Set up signal map
  with context:
    guard()


if __name__ == "__main__":
  main()
