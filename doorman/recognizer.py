# Class to handle checking authorization and dispatching of events
import hashlib
import threading

from lockfile import FileLock

class Recognizer(object):
  def __init__(self, db_name="db.acl"):
    self.db_name = db_name

  def check(self, input):
    hasher = hashlib.sha512()
    hasher.update(input)

    with FileLock(self.db_name):
      for line in open(self.db_name, "r"):
        if line[:-1] == hasher.hexdigest():
          return True

    return False


  def verify(self, input, onTrue=None, onFalse=None):
    """Check input in a new thread, and execute a callback."""

    def check_and_callback():
      if self.check(input) and onTrue:
        onTrue()
      elif onFalse:
        onFalse()

    Thread(group=None, target=check_and_callback).start()

