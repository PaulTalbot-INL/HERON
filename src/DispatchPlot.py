# Copyright 2020, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
  Author: dylanjm
  Date: 2021-05-18
"""
import os
import sys
import itertools as it
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


  @staticmethod
  def _group_by(iterable):
    """
      @ In, iterable, list, a list of column names to group-by.
      @ Out, gr, dict, a dictionary containing a mapping of grouped variable names.
    """
    gr = {}
    for var in iterable:
      key = var.split('__')[-1]
      if key in gr.keys():
        gr[key].append(var)
      else:
        gr[key] = [var]
    return gr

  def run(self):
    """
    """
    df = self._source.asDataset().to_dataframe().reset_index()
    dispatch_vars = list(filter(lambda x: "Dispatch__" in x, df.columns))
    grouped_vars = self._group_by(dispatch_vars)

    for sample_id in df.iloc[:, 0].unique():
      for macro_step in df.iloc[:, 2].unique():
        dat = df[(df.iloc[:, 2] == macro_step) & (df.iloc[:, 0] == sample_id)]
        fig = plt.figure()
        for i, (key, group) in enumerate(grouped_vars.items()):
          ax = fig.add_subplot(len(grouped_vars),1,i+1)
          for var in group:
            ax.plot(dat.iloc[:, 1], dat[var], label=var.replace('__', ' ').title())
            ax.set_xlabel('Time')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        fig.savefig(f"debug_dispatch_{sample_id}_{macro_step}.png")
        plt.clf()
