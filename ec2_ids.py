#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
import sys
from functions import *


class IdsForm(QDialog):
    def __init__(self,parent):
        super(IdsForm,self).__init__(parent)
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("AWS API Manager")
        ids = loadIDS()

        self.user = QLineEdit(ids["user"])
        self.password = QLineEdit(ids["password"])
        self.region = QLineEdit(ids["region"])

        self.mainLayout = QVBoxLayout()

        self.keys = QGridLayout()
        self.keys.addWidget(QLabel("API User"), 0, 0)
        self.keys.addWidget(QLabel("API Password"), 1, 0)
        self.keys.addWidget(QLabel("Region"), 2, 0)

        self.keys.addWidget(self.user,0,1)
        self.keys.addWidget(self.password,1,1)
        self.keys.addWidget(self.region,2,1)

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
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IdsForm(None)
    window.show()
    sys.exit(app.exec_())
    #app.exec_()





