#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from modules.functions import *
from modules import SettingsManager as sm, functions
import platform

class userForm(QDialog):
    def __init__(self,parent):
        super(userForm, self).__init__(parent)
        self.settings = sm.settingsManager()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("Team Setup")

        self.mainLayout = QVBoxLayout()

        self.user = QLineEdit()

        self.save = QPushButton("save")
        self.save.clicked.connect(self.fn_save)

        self.mainLayout.addWidget(self.user)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def fn_save(self):
        cmd = 'useradd {} -m -G wheel'.format(self.user.text())
        settings = SettingsManager.settingsManager()
        settings.setParam("user",self.user.text())
        settings.writeParams()
        print(cmd)
        functions.run_script(cmd)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = userForm(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





