#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from PySide2.QtGui import *
import boto3
import time
#import os
from modules.form_aws_keys import IdsForm
from modules.functions import *
from modules import tabMain, tabSetup
import configparser


class mainWindow(QMainWindow):
    def __init__(self,parent):
        super(mainWindow,self).__init__(parent)

        self.setMinimumWidth(500)
        self.setWindowTitle("EC2 Admin")
        self.setWindowIcon(QIcon(resource_path(os.path.join('files','ec2.png') )))

        self.setCentralWidget(mainWidget(self))

class mainWidget(QWidget):
    def __init__(self,parent):
        super(mainWidget,self).__init__(parent)

        # Definir Layout
        tabs = QTabWidget()
        self.main_tab = tabMain.tabMain(self)
        self.setup_tab = tabSetup.tabSetup(self)

        tabs.addTab(self.main_tab, "Main")
        tabs.addTab(self.setup_tab, "Setup")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.show()

    def getKeys(self):
        self.main_tab.getKeys()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow(None)
    window.show()
    #sys.exit(app.exec_())
    app.exec_()
