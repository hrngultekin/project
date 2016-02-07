# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/connectionitem.ui'
#
# Created: Thu Jan  6 08:35:08 2011
#      by: PyQt5 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ConnectionItem(object):
    def setupUi(self, ConnectionItem):
        ConnectionItem.setObjectName(_fromUtf8("ConnectionItem"))
        ConnectionItem.resize(348, 36)
        ConnectionItem.setMinimumSize(QtCore.QSize(0, 36))
        ConnectionItem.setMaximumSize(QtCore.QSize(16777215, 38))
        self.gridLayout = QtWidgets.QGridLayout(ConnectionItem)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setSpacing(6)
        self.mainLayout.setContentsMargins(3, -1, 3, -1)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.icon = QtWidgets.QLabel(ConnectionItem)
        self.icon.setMinimumSize(QtCore.QSize(32, 32))
        self.icon.setMaximumSize(QtCore.QSize(32, 32))
        self.icon.setText(_fromUtf8(""))
        self.icon.setScaledContents(True)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.mainLayout.addWidget(self.icon)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(-1, 3, -1, 3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.name = QtWidgets.QLabel(ConnectionItem)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setText(_fromUtf8("connection"))
        self.name.setObjectName(_fromUtf8("name"))
        self.verticalLayout.addWidget(self.name)
        self.details = QtWidgets.QLabel(ConnectionItem)
        font = QtGui.QFont()
        self.details.setFont(font)
        self.details.setText(_fromUtf8("details"))
        self.details.setObjectName(_fromUtf8("details"))
        self.verticalLayout.addWidget(self.details)
        self.mainLayout.addLayout(self.verticalLayout)
        self.widget = QtWidgets.QWidget(ConnectionItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.button = QtWidgets.QPushButton(self.widget)
        self.button.setObjectName(_fromUtf8("button"))
        self.gridLayout_2.addWidget(self.button, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.widget)
        self.mainLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(ConnectionItem)
        QtCore.QMetaObject.connectSlotsByName(ConnectionItem)

    def retranslateUi(self, ConnectionItem):
        ConnectionItem.setWindowTitle(QtWidgets.QApplication.translate("ConnectionItem", "ConnectionItem"))
        self.button.setText(QtWidgets.QApplication.translate("ConnectionItem", "Connect"))

