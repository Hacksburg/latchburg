import os
import unittest
from doorman.recognizer import Recognizer

class TestRecognizer(unittest.TestCase):
  def setUp(self):
    self.dir = os.path.dirname(__file__)
    self.r = Recognizer(db_name=os.path.join(self.dir, "testhash.acl"))

    def test_files(self):
      for line in open(os.path.join(self.dir, "testpasswords.txt"), "r"):
        self.assertTrue(self.r.check(line[:-1]))
      self.assertFalse(self.r.check("notpresent"))


if __name__ == "__main__":
  unittest.main()
