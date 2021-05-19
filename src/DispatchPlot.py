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

from PluginBaseClasses.OutStreamPlotPlugin import PlotPlugin, InputTypes, InputData

class DispatchPlot(PlotPlugin):

  @classmethod
  def getInputSpecification(cls):
    """
      Define the acceptable user inputs for this class.
      @ In, None
      @ Out, specs, InputData.ParameterInput,
    """
    specs = super().getInputSpecification()
    # specs.addSub(InputData.parameterInputFactory('variables', contentType=InputTypes.StringListType))
    specs.addSub(InputData.parameterInputFactory('source', contentType=InputTypes.StringType))
    return specs

  def __init__(self):
    """
      Constructor.
      @ In, None
      @ Out, None
    """
    super().__init__()
    self.printTag = 'HERON.DispatchPlot'
    # self._vars = None
    self._sourceName = None
    self._source = None

  def handleInput(self, spec):
    """
    """
    super().handleInput(spec)
    for node in spec.subparts:
      # if node.getName() == 'variables':
      #   self._vars = node.value
      if node.getName() == 'source':
        self._sourceName = node.value

  def initialize(self, stepEntities):
    """
    """
    super().initialize(stepEntities)
    src = self.findSource(self._sourceName, stepEntities)
    if src is None:
      self.raiseAnError(IOError, f'Source DataObject {self._sourceName} was not found in the Step!')
    self._source = src


  def run(self):
    """
    """
    print("I'm done")
