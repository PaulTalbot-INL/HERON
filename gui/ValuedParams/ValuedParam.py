
import os, sys
from PySide2 import QtCore, QtWidgets

HERON_PATH = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'src'))
sys.path.append(HERON_PATH)
from ValuedParams import Factory
allowable = Factory.allowable

class ValuedParamWidget(QtWidgets.QWidget):
  def __init__(self, parent=None, allowed=None, kind='singular'):
    super().__init__(parent=parent)
    if allowed is None:
      allowed = allowable[kind]

    self._layout = QtWidgets.QHBoxLayout()
    self._layout.setSpacing(0)
    self._layout.setMargin(0)
    self.setLayout(self._layout)

    self._drop = QtWidgets.QComboBox()
    self._layout.addWidget(self._drop)

    self._stack = QtWidgets.QStackedLayout(self._layout)
    self._stack_items = {}
    self._layout.addItem(self._stack)
    self._drop.activated.connect(self._stack.setCurrentIndex)

    for k, known in enumerate(a for a in Factory.factory.knownTypes() if a in allowed):
      widget = QtWidgets.QWidget()
      layout = QtWidgets.QHBoxLayout()
      widget.setLayout(layout)
      self._stack_items[known] = {
        'widget': widget,
        'layout': layout,
        'index': k,
      }
      self._stack.addWidget(widget)
      self._drop.addItem(known)
    self._populate_fixed_value()
    self._populate_opt_bounds()
    # TODO opt_bounds, variable, ARMA, ROM, Function, activity

  def _populate_fixed_value(self):
    layout = self._stack_items['fixed_value']['layout']
    edit = QtWidgets.QLineEdit('TEST')
    layout.addWidget(edit)
    self._stack_items['fixed_value']['edit'] = edit

  def _populate_opt_bounds(self):
    data = self._stack_items['opt_bounds']
    layout = data['layout']
    lbl = QtWidgets.QLabel()
    lbl.setText('Low:')
    layout.addWidget(lbl)
    data['low_label'] = lbl

    edit_low = QtWidgets.QLineEdit()
    layout.addWidget(edit_low)
    data['edit_low'] = edit_low

    lbl = QtWidgets.QLabel()
    lbl.setText('High:')
    layout.addWidget(lbl)
    data['hi_label'] = lbl

    edit_hi = QtWidgets.QLineEdit()
    layout.addWidget(edit_hi)
    data['edit_hi'] = edit_hi

if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  win = ValuedParamWidget()
  win.show()
  app.exec_()
