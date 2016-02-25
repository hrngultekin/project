#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services

# Copyright (C) 2010-2011, TUBITAK/UEKAE
# 2010 - Gökçen Eraslan <gokcen:pardus.org.tr>
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt5 import Qt

class PApplicationContainer(Qt.QWidget):
    clientClosed=Qt.pyqtSignal()
    processFinished=Qt.pyqtSignal([int,int])
    
    
    def __init__(self, parent = None, process = None, args = ()):
        Qt.QWidget.__init__(self, parent)
        
        self.layout = Qt.QGridLayout(self)
        self._label = None
        self._proc = None
        self._process = process
        self._args = args
        
        self.container=Qt.QWindow.fromWinId(self.winId())
        self.display=self.createWindowContainer(self.container,self)
        self.layout.addWidget(self.display)
        
        self.parent=parent
        self.pwinId=parent.winId()

    def start(self, process = None, args = ()):
        
        process = process or self._process
        args = args or self._args

        if not process:
            return (False, "Executable not given")

        self._process = process
        self._args = args

        self._proc = Qt.QProcess(self.container)
        self._proc.finished.connect(self._finished)
        self._proc.start(process, args)
        
        print self.getWID()
        self.clientClosed.connect(self._proc.close)

        return (True, "'%s' process successfully started with pid = %s" % (process, self._proc.pid()))

    def closeEvent(self, event):
        if self.isRunning():
            self.clientClosed.emit()
            self._proc.terminate()
            self._showMessage("Terminating process %s" % self._process)
            self._proc.waitForFinished()
        event.accept()

    def _finished(self, exitCode, exitStatus):
        self.processFinished.emit(exitCode, exitStatus)
        if exitCode != 0:
            self._showMessage("%s process finished with code %s" % (self._process, exitCode))
        else:
            self.close()

    def _showMessage(self, message):
        if not self._label:
            self._label = Qt.QLabel(self)

        self._label.setText(message)
        self._label.show()

    def isRunning(self):
        if not self._proc:
            return False
        return not self._proc.state() == Qt.QProcess.NotRunning


    def getWID(self):
        import os
        filename=self._args[0].split("/")[-1]
        
        running=os.system("xwininfo -name \"{} - mpv\"".format(filename))
        if (not running==0):
            return "process NotRunning"
        
        xwininfo=os.popen("xwininfo -name \"{} - mpv\"".format(filename))
        xwininfo_out=xwininfo.read()
        xwininfo.close()
        xwininfo_out=xwininfo_out.split("\n")
        xwininfo_out=xwininfo_out[1]
        winId=xwininfo_out.split(" ")[3]
        return winId
