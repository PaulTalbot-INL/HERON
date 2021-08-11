
"""
TODO
GUI common-use utilities
"""

import inspect
import textwrap
from collections import OrderedDict, UserString
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import * # FIXME limit import

class ResourceComboBox(QtWidgets.QComboBox):
  def __init__(self, model, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._model = model
    self.addItem('Add ...')
    self.addItem('')
    self.addItems(sorted(self._model.resources))
    self.activated.connect(self.on_choose_resource)

  @QtCore.Slot(int)
  def on_choose_resource(self, index):
    if index == 0:
      # Add ...
      text, ok = QtWidgets.QInputDialog.getText(self, 'New Resource', 'New resource name:')
      if ok and text:
        text = text.strip()
        self._model.resources.update([text])
        self.addItem(text)
        self.setCurrentText(text)


##### START from https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
class QStyleSheet(UserString):
    """
    Represent stylesheets as dictionary key value pairs.
    Update complex stylesheets easily modifying only the attributes you need
    Allow for attribute inheritance or defaulting of stylesheets.

    # TODO support [readOnly="true"] attribute-selectors
            QTextEdit, QListView  <-- you can have multiple classes.
            QCheckBox::indicator  <-- some psuedo classes have double colons
    """
    def __init__(self, cls=None, name=None, psuedo=None, **styles):
        """
        Arguments to the constructor allow you to default different properties of the CSS Class.
        Any argument defined here will be global to this StyleSheet and cannot be overidden later.

        :param cls: Default style prefix class to ``cls``
        :param name: Default object name to ``name`` (hashtag) is not needed.
        :param psuedo: Default psuedo class to ``psuedo``, example: ``:hover``
        """
        self.cls_scope = cls
        self.psuedo_scope = psuedo
        self.name_scope = name
        self._styles = OrderedDict() # we'll preserve the order of attributes given - python 3.6+
        if styles:
            self.setStylesDict(OrderedDict(styles))

    def _ident(self, cls=None, name=None, psuedo=None):

        # -- ensure value is of correct type ----------------------------------------
        if cls is not None and not inspect.isclass(cls):
            raise ValueError(f'cls must be None or a class object, got: {type(cls)}')

        if name is not None and not isinstance(name, str):
            raise ValueError(f'name must be None or a str, got: {type(name)}')

        if psuedo is not None and not isinstance(psuedo, str):
            raise ValueError(f'psuedo must be None or a str, got: {type(psuedo)}')

        # -- ensure not overiding defaults -------------------------------------------
        if cls is not None and self.cls_scope is not None:
            raise ValueError(f'cls was set in __init__, you cannot override it')

        if name is not None and self.name_scope is not None:
            raise ValueError(f'name was set in __init__, you cannot override it')

        if psuedo is not None and self.psuedo_scope is not None:
            raise ValueError(f'psuedo was set in __init__, you cannot override it')

        # -- apply defaults if set ---------------------------------------------------
        if cls is None and self.cls_scope is not None:
            cls = self.cls_scope

        if name is None and self.name_scope is not None:
            name = self.name_scope

        if psuedo is None and self.psuedo_scope is not None:
            psuedo = self.psuedo_scope

        # return a tuple that can be used as a dictionary key.
        ident = tuple([getattr(cls, '__name__', None), name or None, psuedo or None])
        return ident

    def _class_definition(self, ident):
        """Get the class definition string"""
        cls, name, psuedo = ident
        return '%s%s%s' % (cls or '', name or '', psuedo or '')

    def _fix_underscores(self, styles):
        return OrderedDict([(k.replace('_', '-'), v) for k,v in styles.items()])

    def setStylesStr(self, styles):
        """
        Parse styles from a string and set them on this object.
        """
        raise NotImplementedError()
        self._update()

    def setStylesDict(self, styles, cls=None, name=None, psuedo=None):
        """
        Set styles using a dictionary instead of keyword arguments
        """
        styles = self._fix_underscores(styles)
        if not isinstance(styles, dict):
            raise ValueError(f'`styles` must be dict, got: {type(styles)}')
        if not styles:
            raise ValueError('`styles` cannot be empty')

        ident = self._ident(cls, name, psuedo)
        stored = self._styles.get(ident, OrderedDict())
        stored.update(styles)
        self._styles[ident] = stored

        self._update()

    def setStyles(self, cls=None, name=None, psuedo=None, **styles):
        """
        Set or update styles according to the CSS Class definition provided by (cls, name, psuedo) using keyword-arguments.

        Any css attribute with a hyphen ``-`` character should be changed to an underscore ``_`` when passed as a keyword argument.

        Example::

            Lets suppose we want to create the css class:

                QFrame#BorderTest { background-color: white; margin:4px; border:1px solid #a5a5a5; border-radius: 10px;}

            >>> stylesheet.setStyle(cls=QFrameBorderTest, background_color='white', margin='4px', border_radius='10px')

            >>> print(stylesheet)

            QFrame#BorderTest { background-color: white; margin:4px; border:1px solid #a5a5a5; border-radius: 10px;}
        """
        styles = OrderedDict(styles)
        self.setStylesDict(styles=styles, cls=cls, name=name, psuedo=psuedo)

    def getStyles(self, cls=None, name=None, psuedo=None):
        """
        Return the dictionary representations of styles for the CSS Class definition provided by (cls, name, psuedo)

        :returns: styles dict (keys with hyphens)
        """
        ident = self._ident(cls, name, psuedo)
        return self._styles.get(ident)

    def getClassIdents(self):
        """Get all class identifier tuples"""
        return list(self._styles.keys())

    def getClassDefinitions(self):
        """Get all css class definitions, but not the css attributes/body"""
        return [self._class_definition(ident) for ident in self.getClassIdents()]

    def validate(self):
        """
        Validate all the styles and attributes on this class
        """
        raise NotImplementedError()

    def merge(self, stylesheet, overwrite=True):
        """
        Merge another QStyleSheet with this QStyleSheet.
        The QStyleSheet passed as an argument will be left un-modified.

        :param overwrite: if set to True the matching class definitions will be overwritten
                          with attributes and values from ``stylesheet``.
                          Otherwise, the css attributes will be updated from ``stylesheet``
        :type overwrite: QStyleSheet
        """
        for ident in stylesheet.getClassIdents():
            styles = stylesheet.getStyles(ident)
            cls, name, psuedo = ident
            self.setStylesDict(styles, cls=cls, name=name, psuedo=psuedo)

        self._update()

    def clear(self, cls=None, name=None, psuedo=None):
        """
        Clear styles matching the Class definition

        The style dictionary cleared will be returned

        None will be returned if nothing was cleared.
        """
        ident = self._ident(cls, name, psuedo)
        return self._styles.pop(ident, None)

    def _update(self):
        """Update the internal string representation"""
        stylesheet = []
        for ident, styles in self._styles.items():
            if not styles:
                continue
            css_cls = self._class_definition(ident)
            css_cls = css_cls + ' ' if css_cls else ''
            styles_str = '\n'.join([f'{k}: {v};' for k, v in styles.items()])

            styles_str = textwrap.indent(styles_str, ''.ljust(4))
            stylesheet.append('%s{\n%s\n}' % (css_cls, styles_str))

        self.data = '\n\n'.join(stylesheet)

##### STILL from https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
class Expander(QWidget):
    def __init__(self, parent=None, title=None, animationDuration=200):
        super().__init__(parent=parent)

        self.animationDuration = animationDuration
        self.toggleAnimation = QtCore.QParallelAnimationGroup()
        self.contentArea = QScrollArea()
        self.headerLine = QFrame()
        self.toggleButton = QToolButton()
        self.mainLayout = QGridLayout()

        toggleButton = self.toggleButton
        self.toggleButtonQStyle = QStyleSheet(QToolButton, border='none')
        toggleButton.setStyleSheet(str(self.toggleButtonQStyle))
        toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toggleButton.setArrowType(QtCore.Qt.RightArrow)
        toggleButton.setText(title or '')
        toggleButton.setCheckable(True)
        toggleButton.setChecked(False)
        toggleButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        headerLine = self.headerLine
        self.headerLineQStyle = QStyleSheet(QFrame)
        headerLine.setFrameShape(QFrame.NoFrame)  # see: https://doc.qt.io/archives/qt-4.8/qframe.html#Shape-enum
        headerLine.setFrameShadow(QFrame.Plain)   # see: https://doc.qt.io/archives/qt-4.8/qframe.html#Shape-enum
        headerLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.contentAreaQStyle = QStyleSheet(QScrollArea, border='none')
        self.contentArea.setStyleSheet(str(self.contentAreaQStyle))
        self.contentArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self.contentArea, b"maximumHeight"))
        # don't waste space
        mainLayout = self.mainLayout
        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        row = 0
        mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        row += 1
        mainLayout.addWidget(self.contentArea, row, 0, 1, 3)
        super().setLayout(self.mainLayout)

        def start_animation(checked):
            arrow_type = QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
            direction = QtCore.QAbstractAnimation.Forward if checked else QtCore.QAbstractAnimation.Backward
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()

        self.toggleButton.clicked.connect(start_animation)

    def setHeaderFrameStyles(self, styles):
        self._setWidgetStyles(self.headerLine, self.headerLineQStyle, styles)

    def setToggleButtonStyles(self, styles):
        self._setWidgetStyles(self.toggleButton, self.toggleButtonQStyle, styles)

    def setContentAreaStyles(self, styles):
        self._setWidgetStyles(self.contentArea, self.contentAreaQStyle, styles)

    def _setWidgetStyles(self, widget, qstylesheet, var):
        if isinstance(var, QStyleSheet):
            qstylesheet.merge(var)
            widget.setStyleSheet(str(qstylesheet))
        elif isinstance(var, dict):
            qstylesheet.setStylesDict(var)
            widget.setStyleSheet(str(qstylesheet))
        elif isinstance(var, str):
            widget.setStyleSheet(var)
        else:
            raise ValueError('invalid argument type: {type(var)}')

    def setLayout(self, contentLayout):
        """
        Set the layout container that you would like to expand/collapse.

        This should be called after all styles are set.
        """
        # Not sure if this is equivalent to self.contentArea.destroy()
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.toggleButton.sizeHint().height()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount()-1):
            spoilerAnimation = self.toggleAnimation.animationAt(i)
            spoilerAnimation.setDuration(self.animationDuration)
            spoilerAnimation.setStartValue(collapsedHeight)
            spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

##### END from https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
