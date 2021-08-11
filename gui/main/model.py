
import os
import sys
import xml.etree.ElementTree as ET
from PySide2 import QtCore

HERON_PATH = os.path.abspath(os.path.expanduser('~/projects/HERON/src')) # FIXME genericize
sys.path.append(HERON_PATH)
import Cases, Components, Placeholders

class HeronSetupModel(QtCore.QObject):
  # signals
  input_changed = QtCore.Signal(dict)
  model_changed = QtCore.Signal(str)

  def __init__(self, app):
    super().__init__()
    self._app = app
    self._xml_root = None   # root of XML for HERON input
    self.resources = set()  # all resources in problem
    #self._filename = None # filename of XML case
    self._param_specs = {'Case': Cases.Case.get_input_specs(),
                         'Component': Components.Component.get_input_specs(),
                         'Source': {'ARMA': Placeholders.ARMA.get_input_specs(),
                                    'Function': Placeholders.Function.get_input_specs(),
                                    'ROM': Placeholders.ROM.get_input_specs()
                                   }
                        } # heirarchal specs for each case

  @property
  def filename(self):
    return self._filename

  @filename.setter
  def filename(self, name):
    self._filename = name
    self._xml_root = ET.parse(name)
    items = {
      'case':    [self._get_identifier(sub, 'Case') for sub in self._xml_root.find('Case')],
      'comps':   [self._get_identifier(sub, 'Components') for sub in self._xml_root.find('Components')],
      'sources': [self._get_identifier(sub, 'DataGenerators') for sub in self._xml_root.find('DataGenerators')]
    }
    self.input_changed.emit(items)
    # load resource set
    for comp in self._xml_root.find('Components'):
      # get basic resources
      self._read_resource_from_attrib(comp.find('produces'))
      self._read_resource_from_attrib(comp.find('demands'))
      self._read_resource_from_attrib(comp.find('stores'))
      # get consumes if a producer
      produces = comp.find('produces')
      if produces:
        consumes = produces.find('consumes')
        if consumes is not None:
          cons = consumes.text
          if cons:
            self.resources.update(x.strip() for x in cons.split(','))

  def _read_resource_from_attrib(self, node):
    if node is not None:
      resources = node.attrib.get('resource', None)
      if resources:
        self.resources.update(x.strip() for x in resources.split(','))

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
