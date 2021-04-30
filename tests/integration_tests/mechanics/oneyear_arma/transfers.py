
# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
  Implements transfer functions
"""

def consume(data, meta):
  activity = meta['HERON']['activity']
  # TODO a get_activity method for the dispatcher -> returns object-safe activity (expression or value)?
  E = -1 * activity['widgets']
  data = {'driver': E}
  return data, meta
