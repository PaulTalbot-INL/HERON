
import os
import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication

from model import HeronSetupModel
from view import HeronSetupView
from control import HeronSetupControl

#DEBUGG
HERON_PATH = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.append(HERON_PATH)
from gui.component.view import ComponentView

class HeronSetupApp(QApplication):

  def __init__(self, sys_argv):
    super().__init__(sys_argv)
    self._model = HeronSetupModel(self)
    self._control = HeronSetupControl(self, self._model)
    self._view = HeronSetupView(self, self._model, self._control)
    self._view.show()
    self._comp_windows = {} # component windows tracking
    # NOTE this doesn't set the app switch name if run through Python.
    # If we launch this with a script, the script may be able to set the name.
    self.setApplicationDisplayName('HERON')

  def edit_component(self, item):
    start_name = item.text()
    # launch component window
    comp_view = self._comp_windows.get(start_name, None)
    if comp_view is None:
      comp_view = ComponentView(self._model, self._control) # TODO pass model, control
      self._comp_windows[start_name] = comp_view
    comp_view.raise_()
    comp_view.show()
    comp_view.setFocus()
    for node in self._model._xml_root.find('Components'):
      if node.attrib['name'] == start_name:
        break
    else:
      raise RuntimeError
    comp_view.load_component(node)
    # save component on return
    # update underlying XML

if __name__ == '__main__':
  app = HeronSetupApp(sys.argv)
  sys.exit(app.exec_())
