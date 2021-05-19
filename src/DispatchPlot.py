# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
  Author: dylanjm
  Date: 2021-05-18
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import _utils as hutils

framework_path = hutils.get_raven_loc()
sys.path.append(framework_path)
from PluginBaseClasses.OutStreamPlotPlugin import PlotPlugin, InputTypes, InputData

class Dispatch(PlotPlugin):

  @classmethod
  def getInputSpecification(cls):
    """
      Define the acceptable user inputs for this class.
      @ In, None
      @ Out, specs, InputData.ParameterInput,
    """
    specs = super().getInputSpecification()
    specs.addSub(InputData.parameterInputFactory('variables', contentType=InputTypes.StringListType))
    specs.addSub(InputData.parameterInputFactory('source', contentType=InputTypes.StringType))
    return specs

  def __init__(self):
    """
      Constructor.
      @ In, None
      @ Out, None
    """
    super().__init__()
    self.printTag = 'HERON.Dispatch'
    self._vars = None
    self._sourceName = None
    self._source = None

  def handleInput(self, spec):
    """
    """
    super().handleInput(spec)
    for node in spec.subparts:
      if node.getName() == 'variables':
        self._vars = node.value
      elif node.getName() == 'source':
        self._sourceName = node.value

  def initialize(self):
    """
    """
    pass

  def run(self):
    """
    """
    pass
