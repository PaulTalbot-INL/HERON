# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
  Author: dylanjm
  Date: 2021-05-18
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PluginBaseClasses.OutStreamPlotPlugin import PlotPlugin, InputTypes, InputData

# Matplotlib Global Settings
plt.rc("figure", figsize=(12, 8), titleweight='bold')
plt.rc(
    "axes",
#     titlesize=25,
    titleweight="bold",
    labelsize=12,
    axisbelow=True,
    grid=True
)
plt.rc("savefig", bbox="tight")
plt.rc("legend", fontsize=12)
plt.rc(["xtick", "ytick"], labelsize=10)


class DispatchPlot(PlotPlugin):

  @classmethod
  def getInputSpecification(cls):
    """
      Define the acceptable user inputs for this class.
      @ In, None
      @ Out, specs, InputData.ParameterInput,
    """
    specs = super().getInputSpecification()
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
    self._sourceName = None
    self._source = None

  def handleInput(self, spec):
    """
    """
    super().handleInput(spec)
    for node in spec.subparts:
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

  def _dispatch_electro(dat, ax):
    """
    """
    pass

  def _dispatch_hydro(dat, ax):
    """
    """
    pass

  def _dispatch_storage(dat, ax):
    """
    """
    pass


  def run(self):
    """
    """
    idx = pd.IndexSlice
    data = self._source.asDataset().to_dataframe()
    data = data.loc[idx[0, :, :, 0]].reset_index()

    dispatch_vars = list(filter(lambda x: "Dispatch__" in x, data.columns))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for var in dispatch_vars:
      ax.plot(data['Time'], data[var])

    fig.savefig("plot.png")
