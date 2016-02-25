#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt5 import QtCore
from PyQt5 import QtWidgets

# PyKDE
from context import *

# UI
from firewallmanager.ui_item import Ui_ItemWidget


class ItemListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent, widget):
        QtWidgets.QListWidgetItem.__init__(self, parent)
        self.widget = widget
        self.setSizeHint(QtCore.QSize(300, 64))

    def getId(self):
        return self.widget.getId()

    def getType(self):
        return self.widget.getType()


class ItemWidget(QtWidgets.QWidget, Ui_ItemWidget):
    #Signal Emits
    stateChanged = QtCore.pyqtSignal([int])
    editClicked = QtCore.pyqtSignal()
    deleteClicked = QtCore.pyqtSignal()
    
    def __init__(self, parent, id_, title="", description="", type_=None, icon=None, state=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.id = id_
        self.type = type_

        self.setTitle(title)
        self.setDescription(description)

        if icon:
            self.setIcon(icon)
        else:
            self.labelIcon.hide()
        if state != None:
            self.setState(state)
        else:
            self.checkState.hide()

        # Buttons
        self.pushEdit.setIcon(KIcon("preferences-other"))
        self.pushDelete.setIcon(KIcon("edit-delete"))

        # Signals
        self.checkState.stateChanged[int].connect(lambda: self.stateChanged[int].emit(self.checkState.checkState()))
        self.pushEdit.clicked.connect(lambda: self.editClicked.emit())
        self.pushDelete.clicked.connect(lambda: self.deleteClicked.emit())

    def mouseDoubleClickEvent(self, event):
        self.pushEdit.animateClick(100)

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def setTitle(self, title):
        self.labelTitle.setText(unicode(title))

    def getTitle(self):
        return unicode(self.labelTitle.text())

    def setDescription(self, description):
        self.labelDescription.setText(unicode(description))

    def getDescription(self):
        return unicode(self.labelDescription.text())

    def setIcon(self, icon):
        self.labelIcon.setPixmap(icon.pixmap(32, 32))

    def getState(self):
        return self.checkState.checkState()

    def setState(self, state):
        if state == True:
            state = QtCore.Qt.Checked
        elif state == False:
            state = QtCore.Qt.Unchecked
        return self.checkState.setCheckState(state)

    def hideEdit(self):
        self.pushEdit.hide()

    def hideDelete(self):
        self.pushDelete.hide()
