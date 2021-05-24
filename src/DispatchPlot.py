# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
  Author: dylanjm
  Date: 2021-05-18
"""
import os
import sys
from itertools import groupby
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PluginBaseClasses.OutStreamPlotPlugin import PlotPlugin, InputTypes, InputData

# Matplotlib Global Settings
plt.rc("figure", figsize=(12, 8), titleweight='bold')
plt.rc(
  "axes",
  #titlesize=25,
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


  def run(self):
    """
    """
    idx = pd.IndexSlice
    data = self._source.asDataset().to_dataframe()
    data = data.loc[idx[0, :, 10, 0]].reset_index()

    dispatch_vars = filter(lambda x: "Dispatch__" in x, data.columns)
    grouped_resources = groupby(dispatch_vars, lambda x: x.split('__')[-1])

    fig = plt.figure()
    # TODO Add loop for Years and _ROM_Clusters
    for i, (key, group) in enumerate(grouped_resources):
      ax = fig.add_subplot(2,1,i+1)
      for var in group:
        # NOTE I don't think we can rely on 'Time' being the unique time-dependent variable.
        ax.plot(data['Time'], data[var], label=var.replace('__', ' ').title())
        ax.set_xlabel('Time')
      ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig.savefig("debug_dispatch.png")
