import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
import test_m
import test_e

def postprocess(jsondata):
    jsondata["output"] = ("Ignore all scores related to autograding; "
                          "just pay attention to the results of the tests.")
    jsondata["score"] = 0
    print(jsondata)


suite = unittest.defaultTestLoader.loadTestsFromModule(test_m)
suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_e))
with open('/autograder/results/results.json', 'w') as f:
    JSONTestRunner(visibility='visible', stream=f, post_processor=postprocess).run(suite)
