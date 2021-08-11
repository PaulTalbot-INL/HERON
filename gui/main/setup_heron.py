
import os
import sys
import xml.etree.ElementTree as ET
from PySide2 import QtCore
from PySide2.QtWidgets import (QApplication, QMainWindow, QDialog,
                               QLineEdit, QPushButton, QScrollArea, QLabel, QTreeWidget,
                               QListWidget,
                               QGridLayout, QHBoxLayout)
from PySide2.QtGui import QPalette, QPixmap

HERON_PATH = os.path.abspath(os.path.expanduser('~/projects/HERON/src')) # FIXME genericize
sys.path.append(HERON_PATH)
import Cases, Components, Placeholders

class CaseSetupWindow(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)
    # member initialization
    self._xml_root = None # root of XML for HERON input
    self._filename = None # filename of XML case
    self._param_specs = {'Case': Cases.Case.get_input_specs(),
                         'Component': Components.Component.get_input_specs(),
                         'Source': {'ARMA': Placeholders.ARMA.get_input_specs(),
                                    'Function': Placeholders.Function.get_input_specs(),
                                    'ROM': Placeholders.ROM.get_input_specs()
                                   }
                        } # heirarchal specs for each case
    # deploy GUI
    self.setWindowTitle('HERON Setup Summary')

    self._case_box_label    = QLabel()
    self._comps_box_label   = QLabel()
    self._sources_box_label = QLabel()

    self._case_box    = QListWidget()
    self._comps_box   = QListWidget()
    self._sources_box = QListWidget()

    self._case_box_desc    = QLabel()
    self._comps_box_desc   = QLabel()
    self._sources_box_desc = QLabel()

    self._case_box_label.   setText('Case')
    self._comps_box_label.  setText('Components')
    self._sources_box_label.setText('Sources')

    self._case_box_desc.   setText('Select an entry for details ...')
    self._comps_box_desc.  setText('Select an entry for details ...')
    self._sources_box_desc.setText('Select an entry for details ...')
    self._case_box_desc.   setStyleSheet('border: 1px solid black;')
    self._comps_box_desc.  setStyleSheet('border: 1px solid black;')
    self._sources_box_desc.setStyleSheet('border: 1px solid black;')

    layout = QGridLayout(self)
    layout.addWidget(self._case_box_label,    0, 0, 1, 1)
    layout.addWidget(self._case_box,          1, 0, 1, 1)
    layout.addWidget(self._case_box_desc,     2, 0, 1, 1)
    layout.addWidget(self._comps_box_label,   0, 1, 1, 1)
    layout.addWidget(self._comps_box,         1, 1, 1, 1)
    layout.addWidget(self._comps_box_desc,    2, 1, 1, 1)
    layout.addWidget(self._sources_box_label, 0, 2, 1, 1)
    layout.addWidget(self._sources_box,       1, 2, 1, 1)
    layout.addWidget(self._sources_box_desc,  2, 2, 1, 1)

    button_layout = QHBoxLayout()
    layout.addLayout(button_layout, 3, 2, 1, 1)
    self._save_button = QPushButton('Save')
    self._load_button = QPushButton('Load')
    self._quit_button = QPushButton('Quit')
    button_layout.addWidget(self._save_button)
    button_layout.addWidget(self._load_button)
    button_layout.addWidget(self._quit_button)

    debug_btn_layout = QHBoxLayout()
    layout.addLayout(debug_btn_layout, 3, 1, 1, 1)
    self._first_opt = QPushButton('Nice')
    self._second_opt = QPushButton('Easy')
    self._third_opt = QPushButton('Other?')
    debug_btn_layout.addWidget(self._first_opt)
    debug_btn_layout.addWidget(self._second_opt)
    debug_btn_layout.addWidget(self._third_opt)

    self.setLayout(layout)

    self._load_case(os.path.join(HERON_PATH, '..', 'tests', 'integration_tests', 'workflows', 'production_flex', 'heron_input.xml'))
    # DEBUGG actually load from XML!
    self._case_box.currentItemChanged.   connect(self._case_index_changed)
    self._comps_box.currentItemChanged.  connect(self._comps_index_changed)
    self._sources_box.currentItemChanged.connect(self._sources_index_changed)

  def _case_index_changed(self, item):
    msg = self._build_xml_output(item.text(), 'Case')
    self._case_box_desc.setText(msg)

  def _comps_index_changed(self, item):
    msg = self._build_xml_output(item.text(), 'Components')
    self._comps_box_desc.setText(msg)

  def _sources_index_changed(self, item):
    msg = self._build_xml_output(item.text(), 'DataGenerators')
    self._sources_box_desc.setText(msg)

  # loading case from XML
  def _load_case(self, fname):
    self._filename = fname
    self._xml_root = ET.parse(fname)
    items = [self._get_identifier(sub, 'Case') for sub in self._xml_root.find('Case')]
    self._case_box.addItems(items)
    items = [self._get_identifier(sub, 'Components') for sub in self._xml_root.find('Components')]
    self._comps_box.addItems(items)
    items = [self._get_identifier(sub, 'DataGenerators') for sub in self._xml_root.find('DataGenerators')]
    self._sources_box.addItems(items)

  def _build_xml_output(self, selected, target_node):
    msg = ''#- Details -'
    if self._xml_root is None:
      case = None
    else:
      case = self._xml_root.find(target_node)
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


if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = CaseSetupWindow()
  win.show()
  sys.exit(app.exec_())
