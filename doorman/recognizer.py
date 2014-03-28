"""Class to handle checking authorization and dispatching of events"""
import hashlib
import threading

from lockfile import FileLock

class Recognizer(object):
  """Verifies hashed entrance attempts"""

  def __init__(self, db_name="db.acl"):
    self.db_name = db_name

  def check(self, input):
    """return True if the hash of the input is in the access list, False otherwise."""

    hasher = hashlib.sha512()
    hasher.update(input)
    digest = hasher.hexdigest()

    # FileLock prevents others (other threads) from editing the file while we're reading it
    with FileLock(self.db_name):
      for line in open(self.db_name, "r"):
        if line[:-1] == digest:
          return digest

    return None
