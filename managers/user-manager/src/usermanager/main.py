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

import commands

# PyQt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
# PyKDE
#from PyKDE4 import kdeui
#from PyKDE4 import kdecore


# UI
from usermanager.ui_main import Ui_MainWidget

# Backend
from usermanager.backend import Interface

# Config
from usermanager.config import DEFAULT_GROUPS, ANIM_SHOW, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME

#Context

from context import *

# Item widget
from usermanager.item import ItemListWidgetItem, ItemWidget

# Edit widget
from usermanager.edit import EditUserWidget, EditGroupWidget

# Delete Dialog
from usermanager.question import DialogQuestion

class MainWidget(QtWidgets.QWidget, Ui_MainWidget):
    def __init__(self, parent, embed=False):
        QtWidgets.QWidget.__init__(self, parent)

        if embed:
            self.setupUi(parent)
        else:
            self.setupUi(self)

        self._in_progress = False

        # Animation
        self.animator = QtCore.QTimeLine(ANIM_TIME, self)

        # Initialize heights of animated widgets
        self.hideEditBox()

        # Backend
        self.iface = Interface()

        # Fail if no packages provide backend
        self.checkBackend()

        # Build "Add New" menu
        self.buildMenu()

        # Build filter
        self.buildFilter()

        # Build item list
        self.buildItemList()

        # User/group edit widgets
        layout = QtWidgets.QVBoxLayout(self.frameWidget)
        self.widgetUserEdit = EditUserWidget(self.frameWidget)
        layout.addWidget(self.widgetUserEdit)
        self.widgetGroupEdit = EditGroupWidget(self.frameWidget)
        layout.addWidget(self.widgetGroupEdit)

        # List user shells
        self.widgetUserEdit.listShells()

        # Signals
        self.comboFilter.currentIndexChanged[int].connect(self.slotFilterChanged)
        self.pushNew.triggered[QAction].connect(self.slotOpenEdit)
        self.buttonBox.accepted.connect(self.slotSaveEdit)
        self.buttonBox.accepted.connect(self.widgetUserEdit.checkFields)
        self.buttonBox.rejected.connect(self.slotCancelEdit)
        self.animator.frameChanged[int].connect(self.slotAnimate)
        self.animator.finished.connect(self.slotAnimationFinished)
        self.widgetUserEdit.buttonStatusChanged[int].connect(self.slotButtonStatusChanged)
        self.widgetGroupEdit.buttonStatusChanged[int].connect(self.slotButtonStatusChanged)

    def hiddenListWorkaround(self):
        """
            Workaround for hidden list items
        """
        size = self.size()
        size += QtCore.QSize(1,1)
        self.resize(size)
        size -= QtCore.QSize(1,1)
        QtCore.QTimer.singleShot(1, lambda: self.resize(size))

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
           QMessageBox.critical(self,"Error", i18n("There are no packages that provide backend for this application.\nPlease make sure that packages are installed and configured correctly"))
           return False
        return True

    def clearItemList(self):
        """
            Clears item list.
        """
        self.listItems.clear()

    def makeItemWidget(self, id_, title="", description="", type_=None, icon=None, state=None):
        """
            Makes an item widget having given properties.
        """
        widget = ItemWidget(self.listItems, id_, title, description, type_, icon, state)
        
        widget.stateChanged[int].connect(self.slotItemState)
        widget.editClicked.connect(self.slotItemEdit)
        widget.deleteClicked.connect(self.slotItemDelete)

        return widget

    def addItem(self, id_, name="", description="", group=False):
        """
            Adds an item to list.
        """
        if group:
            type_ = "group"
            icon = "system-users"
        else:
            type_ = "user"
            icon = "user-identity"

        # Build widget and widget item
        widget = self.makeItemWidget(id_, name, description, type_,KIcon(icon), None)
        widgetItem = ItemListWidgetItem(self.listItems, widget)

        # Groups are uneditable
        if group:
            widget.hideEdit()

        # Add to list
        self.listItems.setItemWidget(widgetItem, widget)

        # Check if a filter matches item
        if not self.itemMatchesFilter(widgetItem):
            self.listItems.itemFromIndex(self.listItems.indexFromItem(widgetItem)).setHidden(True)            
            pass

    def buildItemList(self):
        """
            Builds item list.
        """
        # Clear list
        self.clearItemList()

        # Lists of all users/groups
        self.all_users = []
        self.all_groups = []

        def handleUserList(package, exception, args):
            if exception:
                pass
                # TODO: Handle exception
            else:
                users = args[0]
                for uid, name, fullname in users:
                    self.all_users.append(name)
                    self.addItem(uid, name, fullname)

        self.iface.userList(func=handleUserList)

        def handleGroupList(package, exception, args):
            if exception:
                pass
                # TODO: Handle exception
            else:
                groups = args[0]
                for gid, name in groups:
                    self.all_groups.append(name)
                    self.addItem(gid, name, "", group=True)

        self.iface.groupList(func=handleGroupList)

    def callIface(self, method):
        """
            Grab all comar exceptions
        """
        try:
            method()
        except Exception, e:
            if "Comar.PolicyKit" in e._dbus_error_name:
                QMessageBox.critical(self,"Error", i18n("Access denied"))
            else:
               QMessageBox.critical(self,"Error", unicode(e))
               return False

    def itemMatchesFilter(self, item):
        """
            Checks if item matches selected filter.
        """
        filter = str(self.comboFilter.itemData(self.comboFilter.currentIndex()))
        if filter == "users" and (item.getType() == "group" or item.getId() < 1000 or item.getId() > 65000):
            return False
        elif filter == "groups" and (item.getType() == "user" or item.getId() < 1000 or item.getId() > 65000):
            return False
        elif filter == "all-users" and item.getType() == "group":
            return False
        elif filter == "all-groups" and item.getType() == "user":
            return False
        return True

    def buildFilter(self):
        """
            Builds item filter.
        """
        self.comboFilter.clear()
        self.comboFilter.addItem(i18n("Users"), QtCore.QVariant("users"))
        self.comboFilter.addItem(i18n("Groups"), QtCore.QVariant("groups"))
        self.comboFilter.addItem(i18n("All Users"), QtCore.QVariant("all-users"))
        self.comboFilter.addItem(i18n("All Groups"), QtCore.QVariant("all-groups"))

    def buildMenu(self):
        """
            Builds "Add New" button menu.
        """
        # Create menu for "new" button
        menu = QtWidgets.QMenu(self.pushNew)
        self.pushNew.setMenu(menu)

        # New user action
        action_user = QtWidgets.QAction((i18n("Add User")), self)
        action_user.setData(QtCore.QVariant("user"))
        menu.addAction(action_user)

        # New group action
        action_group = QtWidgets.QAction((i18n("Add Group")), self)
        action_group.setData(QtCore.QVariant("group"))
        menu.addAction(action_group)

    def showEditBox(self, id_, type_):
        """
            Shows edit box.
        """
        self.typeEdit = type_
        if type_ == "user":
            # Reset fields
            self.widgetUserEdit.reset()

            if id_ != None:
                try:
                    username, fullname, gid, homedir, shell, groups = self.iface.userInfo(id_)
                except Exception, e: # TODO: Named exception should be raised
                    if "Comar.PolicyKit" in e._dbus_error_name:
                       QMessageBox.critical(self,"Error",i18n("Access denied"))
                    else:
                        QMessageBox.critical(self,"Error",unicode(e))
                    return
                self.widgetUserEdit._new = False
                self.widgetUserEdit.setId(id_)
                self.widgetUserEdit.setUsername(username)
                self.widgetUserEdit.setFullname(fullname)
                self.widgetUserEdit.setHomeDir(homedir)
                self.widgetUserEdit.setShell(shell)
                self.widgetUserEdit.setGroups(self.all_groups, groups)
                try:
                    self.widgetUserEdit.setAuthorizations(self.iface.getAuthorizations(id_))
                except Exception, e: # TODO: Named exception should be raised
                    if "Comar.PolicyKit" in e._dbus_error_name:
                        QMessageBox.critical(self,"Error",i18n("Access denied"))
                    else:
                        QMessageBox.critical(self,"Error",unicode(e))
                    return
            else:
                authorizations = []
                self.widgetUserEdit._new = True
                self.widgetUserEdit.setShell('/bin/bash')
                self.widgetUserEdit.setNickList(self.all_users)
                self.widgetUserEdit.setGroups(self.all_groups, DEFAULT_GROUPS)
                self.widgetUserEdit.setAuthorizations(authorizations)

            if self.widgetUserEdit.isNew():
                self.widgetUserEdit.checkFields()

            # Hide group edit
            self.widgetGroupEdit.hide()
            # Show user edit
            self.widgetUserEdit.show()

        else:
            # Reset fields
            self.widgetGroupEdit.reset()
            # Hide user edit
            self.widgetUserEdit.hide()
            # Show group edit
            self.widgetGroupEdit.show()

        # Set range
        self.animator.setFrameRange(ANIM_TARGET, self.height() - ANIM_TARGET)
        # Go go go!
        self.animator.start()

    def hideEditBox(self):
        """
            Hides edit box.
        """
        self.frameEdit.setMaximumHeight(ANIM_TARGET)
        self.frameList.setMaximumHeight(ANIM_DEFAULT)
        self.hiddenListWorkaround()

    def slotFilterChanged(self, index):
        """
            Filter is changed, refresh item list.
        """
        for i in range(self.listItems.count()):
            widgetItem = self.listItems.item(i)
            if self.itemMatchesFilter(widgetItem):
                #self.listItems.setItemHidden(widgetItem, False)
                self.listItems.itemFromIndex(self.listItems.indexFromItem(widgetItem)).setHidden(False) 
            else:
                #self.listItems.setItemHidden(widgetItem, True)
                self.listItems.itemFromIndex(self.listItems.indexFromItem(widgetItem)).setHidden(True)   
        self.hiddenListWorkaround()

    def slotItemState(self, state):
        """
            Item state changed.
        """
        pass

    def slotItemEdit(self):
        """
            Edit button clicked, show edit box.
        """
        widget = self.sender()
        if widget.getType() == "user":
            self.showEditBox(widget.getId(), "user")

    def slotItemDelete(self):
        """
            Delete button clicked.
        """
        widget = self.sender()
        if widget.getType() == "user":
            uid = widget.getId()
            username = widget.getTitle()
            fullname = widget.getDescription()

            # If the user is logged in display warning, else delete user
            if self.userLoggedOn(username):
                message =i18n("Cannot delete <b>%1</b>. The user is currently logged in.", username)
                QMessageBox.information(self,'Message',message)

            else:
                dialog = DialogQuestion(self)
                dialog.setQuestion(i18n("Do you want to delete user '%1' (%2)?", fullname, username))
                dialog.setCheckBox(i18n("Also remove user files. (This may take long.)"))
                if dialog.exec_():
                    self.callIface(lambda: self.iface.deleteUser(uid, deleteFiles=dialog.getCheckBox()))
                    # User.Manager does not emit signals, refresh whole list.
                    self.buildItemList()
        else:
            gid = widget.getId()
            groupname = widget.getTitle()
            dialog=DialogQuestion(self)
            dialog.setQuestion(i18n("Do yu want to delete group '%1'?",groupname))
            dialog.checkBox.hide()
            if dialog.exec_():
                 self.callIface(lambda: self.iface.deleteGroup(gid))
                 self.buildItemList()



    def userLoggedOn(self, userToDelete):
        """
            Check if user is logged on.
        """
        loggedOnUsers = commands.getoutput('users')
        return userToDelete in loggedOnUsers

    def slotOpenEdit(self, action):
        """
            New button clicked, show edit box.
        """
        # Get item type to add/
        type_ = str(action.data())
        self.showEditBox(None, type_)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)

    def slotCancelEdit(self):
        """
            Cancel clicked on edit box, show item list.
        """
        self.hideEditBox()

    def slotSaveEdit(self):
        """
            Save clicked on edit box, save item details then show item list.
        """
        if self._in_progress:
            return
        self._in_progress = True
        try:
            self.buttonBox.setDisabled(True)
            if self.typeEdit == "user":
                widget = self.widgetUserEdit
                grant, revoke, block = widget.getAuthorizations()

                if widget.wrn:
                    answer=QtWidgets.QMessageBox.warning(self,i18n("Remove items"),unicode(widget.wrn),QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
                    if answer == QtWidgets.QMessageBox.No:
                        return

                if widget.isNew():
                    self.iface.addUser(widget.getId(), widget.getUsername(), widget.getFullname(), widget.getHomeDir(), widget.getShell(), widget.getPassword(), widget.getGroups(), grant, block)
                else:
                    def handler(package, exception, args):
                        pass
                    self.iface.setUser(widget.getId(), widget.getFullname(), widget.getHomeDir(), widget.getShell(), widget.getPassword(), widget.getGroups())
                    # Revoke
                    for action_id in revoke:
                        self.iface.setRevoke(widget.getId(), action_id)
                    # Grant
                    for action_id in grant:
                        self.iface.setGrant(widget.getId(), action_id)
                    # Block
                    for action_id in block:
                        self.iface.setBlock(widget.getId(), action_id)

            else:
                widget = self.widgetGroupEdit
                self.callIface(lambda: self.iface.addGroup(widget.getId(), widget.getGroupname()))
        except Exception, e: # TODO: Named exception should be raised
            if "Comar.PolicyKit" in e:
                QMessageBox.critical(self,"Error",i18n("Access denied"))
            else:
                QMessageBox.critical(self,"Error",unicode(e))
            return
        finally:
            self._in_progress = False
            self.buttonBox.setDisabled(False)

        # Hide edit box
        self.hideEditBox()
        # User.Manager does not emit signals, refresh whole list.
        self.buildItemList()

    def slotAnimate(self, frame):
        """
            Animation frame changed.
        """
        self.frameEdit.setMaximumHeight(frame)
        self.frameList.setMaximumHeight(self.height() - frame)
        self.update()

    def slotAnimationFinished(self):
        """
            Animation is finished.
        """
        self.frameEdit.setMaximumHeight(ANIM_DEFAULT)
        self.frameList.setMaximumHeight(ANIM_TARGET)

    def slotButtonStatusChanged(self, status):
        if status:
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        else:
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
