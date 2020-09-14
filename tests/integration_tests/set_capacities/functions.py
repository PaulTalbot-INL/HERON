
# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
  Implements transfer functions
"""

def consume(data, meta):
  activity = meta['HERON']['activity']
  amount = -1 * activity['widgets']
  data = {'driver': amount}
  return data, meta

# def flex_price(data, meta):
#   sine = meta['HERON']['RAVEN_vars']['Signal']
#   t = meta['HERON']['time_index']
#   # DispatchManager
#   # scale electricity consumed to flex between -1 and 1
#   amount = - 2 * (sine[t] - 0.5)
#   data = {'reference_price': amount}
#   return data, meta
