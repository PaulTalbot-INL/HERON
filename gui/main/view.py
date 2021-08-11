
from PySide2 import QtCore
from PySide2.QtWidgets import (QDialog, QPushButton, QLabel, QListWidget, QGridLayout, QHBoxLayout,
                               QListWidgetItem)

class HeronSetupView(QDialog):
  def __init__(self, app, model, controller, parent=None):
    super().__init__(parent)
    self._app = app
    self._model = model
    self._control = controller

    #listeners
    self._model.input_changed.connect(self.on_input_changed)

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
    self._layout = layout
    layout.addWidget(self._case_box_label,    0, 0, 1, 1)
    layout.addWidget(self._case_box,          1, 0, 1, 1)
    layout.addWidget(self._case_box_desc,     2, 0, 1, 1)
    layout.addWidget(self._comps_box_label,   0, 1, 1, 1)
    layout.addWidget(self._comps_box,         1, 1, 1, 1)
    layout.addWidget(self._comps_box_desc,    2, 1, 1, 1)
    layout.addWidget(self._sources_box_label, 0, 2, 1, 1)
    layout.addWidget(self._sources_box,       1, 2, 1, 1)
    layout.addWidget(self._sources_box_desc,  2, 2, 1, 1)

    case_btn_layout = QHBoxLayout()
    layout.addLayout(case_btn_layout, 3, 0, 1, 1)
    self._case_edit_button = QPushButton('Edit')
    case_btn_layout.addWidget(self._case_edit_button)
    self._case_edit_button.setEnabled(False)

    comp_btn_layout = QHBoxLayout()
    layout.addLayout(comp_btn_layout, 3, 1, 1, 1)
    self._comp_add_button = QPushButton('Add ...')
    self._comp_add_button.clicked.connect(self.on_comp_add)
    self._comp_add_button.setEnabled(False)
    self._comp_edit_button = QPushButton('Edit ...')
    self._comp_edit_button.clicked.connect(self.on_comp_edit)
    self._comp_remove_button = QPushButton('Remove')
    self._comp_remove_button.setEnabled(False)
    comp_btn_layout.addWidget(self._comp_add_button)
    comp_btn_layout.addWidget(self._comp_edit_button)
    comp_btn_layout.addWidget(self._comp_remove_button)

    button_layout = QHBoxLayout()
    layout.addLayout(button_layout, 3, 2, 1, 1)
    self._save_button = QPushButton('&Save')
    self._load_button = QPushButton('&Load')
    self._quit_button = QPushButton('&Quit')
    button_layout.addWidget(self._save_button)
    button_layout.addWidget(self._load_button)
    button_layout.addWidget(self._quit_button)
    self._save_button.setEnabled(False)
    self._load_button.clicked.connect(self._control.load_input)
    self._quit_button.clicked.connect(self._app.exit)

    self.setLayout(layout)

    self._case_box.currentItemChanged   .connect(self.on_case_index_changed)
    self._comps_box.currentItemChanged  .connect(self.on_comps_index_changed)
    self._sources_box.currentItemChanged.connect(self.on_sources_index_changed)

  # input file
  @QtCore.Slot(dict)
  def on_input_changed(self, items):
    self._case_box.addItems(items['case'])
    self._comps_box.addItems(items['comps'])
    self._sources_box.addItems(items['sources'])

  # selecting from item boxes
  @QtCore.Slot(QListWidgetItem)
  def on_case_index_changed(self, item):
    msg = self._control._build_xml_output(item.text(), 'Case')
    self._case_box_desc.setText(msg)

  @QtCore.Slot(QListWidgetItem)
  def on_comps_index_changed(self, item):
    msg = self._control._build_xml_output(item.text(), 'Components')
    self._comps_box_desc.setText(msg)

  @QtCore.Slot(QListWidgetItem)
  def on_sources_index_changed(self, item):
    msg = self._control._build_xml_output(item.text(), 'DataGenerators')
    self._sources_box_desc.setText(msg)

  # modifying lists
  @QtCore.Slot()
  def on_comp_add(self):
    TODO

  @QtCore.Slot()
  def on_comp_edit(self):
    self._app.edit_component(self._comps_box.currentItem())
