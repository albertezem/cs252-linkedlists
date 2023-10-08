#!/usr/bin/python3

import unittest
import test_utilities
from gradescope_utils.autograder_utils.decorators import weight

class Tests(unittest.TestCase):
  @weight(1)
  def testCode(self):
    return_value = test_utilities.runIt('')
    if return_value != None:
        self.fail(return_value)
