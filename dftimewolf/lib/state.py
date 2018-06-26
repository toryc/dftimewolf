"""This class maintains the internal dfTimewolf state.

Use it to track errors, abort on global failures, cleanup after modules, etc.
"""
# TODO(tomchop): Make sure docstrings here follow the same type hinting as the
# rest of the codebase
from __future__ import print_function
from __future__ import unicode_literals

import sys

class DFTimewolfState(object):
  """The main State class.

  Attributes:
    errors: [(str, bool)] The errors generated by a module. These should be
        cleaned up after each module run using the cleanup() method.
    global_errors: [(str, bool)] the cleanup() method moves non critical errors
        to this attribute for later reporting.
    current_module: The DFTimewolfModule module that is currently executing.
    input: list, The data that the current module will use as input.
    output: list, The data that the current module generates.
  """

  def __init__(self):
    self.errors = []
    self.global_errors = []
    self.current_module = None
    self.input = []
    self.output = []

  def add_error(self, error, critical=False):
    """Adds an error to the state.

    Args:
      error: The text that will be added to the error list.
      critical: If set to True and the error is checked with check_errors, will
          dfTimewolf will abort.
    """
    self.errors.append((error, critical))

  def set_current_module(self, module):
    """Sets the current_module for the state.

    Args:
      module: The dfTimewolfModule to define as current module.
    """
    self.current_module = module

  def cleanup(self):
    """Basic cleanup after modules.

    The state's output becomes the input for the next stage. Any errors are
    moved to the global_errors attribute so that they can be reported at a
    later stage.
    """
    # Move any existing errors to global errors
    self.global_errors.extend(self.errors)
    self.errors = []

    # Make the previous module's output available to the next module
    self.input = self.output
    self.output = []

  def check_errors(self, is_global=False):
    """Checks for errors and exits if any of them are critical.

    Args:
      is_global: If True, check the global_errors attribute. If false, check the
          error attribute.
    """
    errors = self.global_errors if is_global else self.errors
    if errors:
      print('dfTimewolf encountered one or more errors:')
      for error, critical in errors:
        print('{0:s}  {1:s}'.format('CRITICAL: ' if critical else '', error))
        if critical:
          print('Critical error found. Aborting.')
          sys.exit(-1)
