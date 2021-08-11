
import os
import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QFileDialog

HERON_PATH = os.path.abspath(os.path.expanduser('~/projects/HERON/src')) # FIXME genericize
sys.path.append(HERON_PATH)
import Cases, Components, Placeholders

class HeronSetupControl(QtCore.QObject):
  def __init__(self, app, model):
    super().__init__()
    self._app = app
    self._model = model

  # loading case from XML
  @QtCore.Slot()
  def load_input(self):
    filename = QFileDialog.getOpenFileName(self._app._view, 'Open HERON input', os.path.join(HERON_PATH, '..'),
        'HERON inputs (*.xml)')[0]
    self._model.filename = filename
    # self._xml_root = ET.parse(self._filename)
    # items = [self._get_identifier(sub, 'Case') for sub in self._xml_root.find('Case')]
    # self._case_box.addItems(items)
    # items = [self._get_identifier(sub, 'Components') for sub in self._xml_root.find('Components')]
    # self._comps_box.addItems(items)
    # items = [self._get_identifier(sub, 'DataGenerators') for sub in self._xml_root.find('DataGenerators')]
    # self._sources_box.addItems(items)

  def _build_xml_output(self, selected, target_node):
    msg = ''#- Details -'
    root = self._model._xml_root # TODO getter
    if root is None:
      case = None
    else:
      case = root.find(target_node)
    if case is None:
      msg += f'- No <target_node> found! -'
    else:
      for sub in case:
        if self._get_identifier(sub, target_node) == selected:
          msg = self._xml_fill(msg, sub)
          break
    return msg

  def _get_identifier(self, node, kind):
    if kind == 'Case':
      return node.tag
    elif kind == 'Components':
      return node.attrib.get('name', '')
    elif kind == 'DataGenerators':
      return f'{node.tag}: {node.attrib.get("name", "")}'

  def _xml_fill(self, msg, node, t=0):
    value = node.text.strip() if node.text is not None else ""
    if len(node) or len(value):
      sep = ':'
    else:
      sep = ''
    tab = '  '
    pre = '\n' if len(msg) > 0 else ''
    msg += f'{pre}{tab*t}{node.tag}{sep} {node.text.strip() if node.text is not None else ""}'
    for key, val in node.attrib.items():
      msg += f'\n{tab*(t+1)}{key}: {val}'
    for sub in node:
      msg = self._xml_fill(msg, sub, t=t+1)
    return msg
