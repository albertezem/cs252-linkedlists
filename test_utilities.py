#!/usr/bin/python3

import subprocess
import sys
import unittest
import signal
from typing import Optional
import os
import collections

TestResult = collections.namedtuple('TestResult', ['output', 'error'])

def runcmd(cmd, input_text=None):
  splitcmd=cmd.split()
  return subprocess.run(splitcmd, input=input_text,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE, encoding='utf-8')

def buildCode() -> Optional[str]:

  # Make sure that warnings aren't suppressed
  for filename in os.listdir():
    split_filename = os.path.splitext(filename)
    if split_filename[1] in ['.c', '.h']:
      with open(filename, 'r') as f:
        for line in f.readlines():
          if 'diagnostic' in line and 'ignore' in line:
            return 'Please do not disable warnings.'

  # Compile, show output
  compile_return = runcmd('just build')
  print(compile_return.stdout)

  # Make sure that warning causes test to fail
  if ('warning' in compile_return.stdout):
    return 'Test failed because of compiler warning.'

  return None

def runIt(test_input):
  error = buildCode()
  if error != None:
    return error

  # Run it once without valgrind
  process_out = runcmd('./linkedlist ' + test_input)
  print(process_out.stdout)

  # If segfaults, run it again with valgrind to show
  if process_out.returncode != 0 and process_out.returncode != -signal.SIGSEGV:
    return "Runtime error."

  # Run it again with valgrind
  valgrind_test_results = run_tests_with_valgrind(
                './linkedlist ' + test_input)
  if valgrind_test_results.error:
    print('---VALGRIND ERROR---')
    print('Valgrind test results')
    print(valgrind_test_results.output)
    return "Valgrind error."
  else:
    print('---VALGRIND NO ERROR---')

  return None
  
  
def run_tests_with_valgrind(executable_command) -> TestResult:
    '''Run again with valgrind (just student version) and look for errors)'''
    valgrind_command = \
        'ulimit -c 0 && ' + \
        'valgrind ' + \
        '--leak-check=full ' + \
        '--show-leak-kinds=all ' + \
        '--errors-for-leak-kinds=all ' + \
        '--error-exitcode=99 ' + \
        executable_command

    try:
        process = subprocess.run(
            valgrind_command,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=10,
            shell=True)

        # Verify that there is no error from Valgrind.
        #  This looks for the presence of the string
        # "0 errors from 0 contexts" which is that Valgrind prints when
        # no errors.
        valgrind_error_location = (
            process.stdout
            .decode('utf-8')
            .find("ERROR SUMMARY: 0 errors from 0 contexts")
        )
        valgrind_error_found = valgrind_error_location == -1
        return TestResult(process.stdout.decode('utf-8'),
                          valgrind_error_found)
    except subprocess.TimeoutExpired:
        return TestResult("Timed out", True)
