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

#Context
from context import *
# UI
from firewallmanager.ui_service import Ui_ServiceWidget


class ServiceWidget(QtWidgets.QWidget, Ui_ServiceWidget):
    stateChanged = QtCore.pyqtSignal([int])
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.state = False

        # Signals
        self.pushToggle.clicked.connect(lambda: self.stateChanged[int].emit(not self.getState()))

    def setState(self, state):
        self.state = state
        if state:
            self.labelStatus.setText(i18n("Firewall is activated."))
            self.labelIcon.setPixmap(KIcon("document-encrypt").pixmap(48, 48))
            self.pushToggle.setIcon(KIcon("media-playback-stop"))
            self.pushToggle.setText(i18n("Stop"))
        else:
            self.labelStatus.setText(i18n("Firewall is deactivated."))
            self.labelIcon.setPixmap(KIcon("document-decrypt").pixmap(48, 48))
            self.pushToggle.setIcon(KIcon("media-playback-start"))
            self.pushToggle.setText(i18n("Start"))

    def getState(self):
        return self.state

    def setEnabled(self, enabled):
        self.pushToggle.setEnabled(enabled)
