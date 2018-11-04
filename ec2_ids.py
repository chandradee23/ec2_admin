#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PyQt5.QtWidgets import *
import re
import os
import sys
from functions import *

scriptDir = os.path.dirname(sys.executable)
config_filename = os.path.join(os.path.expanduser('~')) + "/.config_aws_ec2.cfg"

class IdsForm(QDialog):
    def __init__(self,parent):
        super(IdsForm,self).__init__(parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("AWS API Manager")
        ids = loadIDS()

        self.id = QLineEdit(ids["id_ec2"])
        self.user = QLineEdit(ids["user"])
        self.password = QLineEdit(ids["password"])
        self.region = QLineEdit(ids["region"])

        self.mainLayout = QVBoxLayout()

        self.keys = QGridLayout()
        self.keys.addWidget(QLabel("Instance ID"),0,0)
        self.keys.addWidget(QLabel("API User"), 1, 0)
        self.keys.addWidget(QLabel("API Password"), 2, 0)
        self.keys.addWidget(QLabel("Region"), 3, 0)

        self.keys.addWidget(self.id,0,1)
        self.keys.addWidget(self.user,1,1)
        self.keys.addWidget(self.password,2,1)
        self.keys.addWidget(self.region,3,1)

        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_to_file)

        self.mainLayout.addLayout(self.keys)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def save_to_file(self):
        with open(config_filename, 'w+') as file:
            file.write(self.user.text()+"\n")
            file.write(self.password.text()+"\n")
            file.write(self.region.text()+"\n")
            file.write(self.id.text()+"\n")
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IdsForm(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





