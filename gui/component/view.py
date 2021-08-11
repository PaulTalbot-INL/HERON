
import os, sys

from PySide2 import QtCore, QtWidgets

HERON_PATH = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.append(HERON_PATH)
import gui.gui_utils as gutils
from gui.ValuedParams.ValuedParam import ValuedParamWidget

class ComponentView(QtWidgets.QDialog):
  def __init__(self, model, controller, parent=None, debug=False):
    super().__init__(parent)
    self._model = model # TODO this should be the XML handler?
    self._control = controller
    self._xml = None # TODO move to model?

    #listeners
    ## DEBUGG let us look at layout without setting up connections
    #if model is None and controller is None:
    #  debug = True
      #self._model.component_changed.connect(self.on_component_changed)

    self.setWindowTitle('HERON Component Setup')

    self._main_layout = QtWidgets.QGridLayout(self)
    self._name_lbl = QtWidgets.QLabel()
    self._name_lbl.setText('Component Name:')
    self._name_entry = QtWidgets.QLineEdit() # TODO make this a label with an edit option
    if not debug:
      self._name_entry.editingFinished.connect(self.on_change_name)
      #self._name_entry.returnPressed.connect(self.on_name_return)
    self._main_layout.addWidget(self._name_lbl, 0, 0, 1, 1)
    self._main_layout.addWidget(self._name_entry, 0, 1, 1, 1)

    # TODO make a Physics box and an Economics box using a QScrollArea and some animation stuff
    self._physics_box = QtWidgets.QGroupBox('Physics')
    self._main_layout.addWidget(self._physics_box, 1, 0, 4, 4)
    self._physics_layout = QtWidgets.QGridLayout(self)
    self._physics_box.setLayout(self._physics_layout)

    self._physics_kind_lbl = QtWidgets.QLabel()
    self._physics_kind_lbl.setText('Component Type:')
    self._physics_layout.addWidget(self._physics_kind_lbl, 0, 0, 1, 1)
    self._physics_kind_drp = QtWidgets.QComboBox()
    self._physics_kind_drp.activated.connect(self.on_choose_physics_type)
    self._physics_layout.addWidget(self._physics_kind_drp, 0, 1, 1, 1)

    # here we have the hot-swappable component type options
    self._physics_sub = QtWidgets.QStackedLayout()
    self._physics_layout.addLayout(self._physics_sub, 1, 0, 5, 5)
    # layouts
    self._physics_sub_entries = {}
    options = ['Choose ...', 'Generator', 'Sink', 'Storage']
    for k, kind in enumerate(options):
      widget = QtWidgets.QWidget()
      layout = QtWidgets.QGridLayout()
      widget.setLayout(layout)
      self._physics_sub_entries[kind] = {'widget': widget,
                                         'layout': layout,
                                         'index': k}
      self._physics_sub.addWidget(widget)
      self._physics_kind_drp.addItem(kind)
    self._populate_physics_generator()
    self._populate_physics_sink()
    self._populate_physics_storage()

    self._close_btn = QtWidgets.QPushButton('Done')
    self._close_btn.setEnabled(False)
    self._main_layout.addWidget(self._close_btn, 7, 2, 1, 1)
    self.setLayout(self._main_layout)

  # modularized populators
  def _populate_physics_generator(self):
    layout = self._physics_sub_entries['Generator']['layout']
    self._physics_generator_consumes_lbl = QtWidgets.QLabel()
    self._physics_generator_consumes_lbl.setText('Consumes:')
    self._physics_generator_consumes = gutils.ResourceComboBox(self._model)
    # self._physics_generator_consumes.activated.connect(self.on_physics_generator_consumes_change)
    # self._physics_generator_consumes.setEditable(True) #QLineEdit()
    # self._physics_generator_consumes.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically) #QLineEdit()
    layout.addWidget(self._physics_generator_consumes_lbl, 0, 0, 1, 1)
    layout.addWidget(self._physics_generator_consumes,     0, 1, 1, 1)

    self._physics_generator_produces_lbl = QtWidgets.QLabel()
    self._physics_generator_produces_lbl.setText('Produces:')
    self._physics_generator_produces = gutils.ResourceComboBox(self._model)
    layout.addWidget(self._physics_generator_produces_lbl, 0, 2, 1, 1)
    layout.addWidget(self._physics_generator_produces,     0, 3, 1, 1)

    row_w = QtWidgets.QWidget()
    row = QtWidgets.QHBoxLayout(self._physics_sub_entries['Generator']['widget'])
    row_w.setLayout(row)
    layout.addWidget(row_w, 1, 0, 1, 5)
    self._physics_generator_cap_row = row
    self._physics_generator_capacity_lbl = QtWidgets.QLabel()
    self._physics_generator_capacity_lbl.setText('Capacity')
    row.addWidget(self._physics_generator_capacity_lbl)
    self._physics_cap_vp = ValuedParamWidget()
    row.addWidget(self._physics_cap_vp)

  def _populate_physics_sink(self):
    layout = self._physics_sub_entries['Sink']['layout']
    self._physics_sink_consumes_lbl = QtWidgets.QLabel()
    self._physics_sink_consumes_lbl.setText('Consumes:')
    self._physics_sink_consumes = QtWidgets.QLineEdit()
    layout.addWidget(self._physics_sink_consumes_lbl, 0, 0, 1, 1)
    layout.addWidget(self._physics_sink_consumes,     0, 1, 1, 1)

  def _populate_physics_storage(self):
    layout = self._physics_sub_entries['Storage']['layout']
    self._physics_storage_stores_lbl = QtWidgets.QLabel()
    self._physics_storage_stores_lbl.setText('Stores:')
    self._physics_storage_stores = QtWidgets.QLineEdit()
    layout.addWidget(self._physics_storage_stores_lbl, 0, 0, 1, 1)
    layout.addWidget(self._physics_storage_stores,     0, 1, 1, 1)

  @QtCore.Slot(int)
  def on_choose_physics_type(self, index):
    self._physics_sub.setCurrentIndex(index)

  @QtCore.Slot()
  def on_change_name(self):
    # TODO move this to after "done"/"save" is clicked
    new = self._name_entry.text()
    if new != self._current_name:
      print('DEBUGG name changed to:', self._name_entry.text())
      self._xml.attrib['name'] = new
      self._current_name = new
    self._name_entry.clearFocus()

  def load_component(self, xml):
    self._xml = xml # TODO move to Model?
    self._current_name = xml.attrib['name']
    self._name_entry.setText(self._current_name)
    # physics
    kind = None
    if xml.find('produces') is not None:
      kind = 'Generator'
      self._load_generator(xml)
    elif xml.find('demands') is not None:
      kind = 'Sink'
      self._load_sink(xml)
    elif xml.find('storage') is not None:
      kind = 'Storage'
      self.load_storage(xml)

    # economics

  def _load_generator(self, xml):
    index = self._physics_sub_entries['Generator']['index']
    self._physics_sub.setCurrentIndex(index)
    self._physics_kind_drp.setCurrentIndex(index)
    node = xml.find('produces')
    produces = node.attrib.get('resource', '')
    self._physics_generator_produces.setCurrentText(produces)
    consumes = node.find('consumes').text.strip() if node.find('consumes') is not None else ''
    self._physics_generator_consumes.setCurrentText(consumes)

if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  win = ComponentView(None, None, parent=None, debug=True)
  win.show()
  app.exec_()
