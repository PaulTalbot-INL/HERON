# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED

from .ExampleValidator import Example
from .RefGovValidator import RefGov

known = {
    'Example': Example,
    'RefGov': RefGov,
    # ModelicaGoverner: TODO,
}

def get_class(typ):
  """
    Returns the requested dispatcher type.
    @ In, typ, str, name of one of the dispatchers
    @ Out, class, object, class object
  """
  return known.get(typ, None)
