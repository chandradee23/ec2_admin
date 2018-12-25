#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from modules.functions import *
from modules import SettingsManager as sm
import os
import re

home = os.path.expanduser("~")

class IdsForm(QDialog):
    def __init__(self,parent):
        super(IdsForm,self).__init__(parent)
        self.settings = sm.settingsManager()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("AWS API Manager")

        self.api_access = QLineEdit(self.settings.getParam('aws_access_key_id'))
        self.api_secret = QLineEdit(self.settings.getParam('aws_secret_access_key'))
        self.api_secret.setEchoMode(QLineEdit.Password)
        region = self.settings.getParam('region')
        self.region = QLineEdit("us-east-2" if region == "" else region)
        self.pem = QPushButton("Select PEM Key File")
        self.pem.clicked.connect(self.fn_pem)

        self.mainLayout = QVBoxLayout()

        self.keys = QGridLayout()
        self.keys.addWidget(QLabel("Api Access"),0,0)
        self.keys.addWidget(self.api_access, 0, 1)
        self.keys.addWidget(QLabel("Api Secret"),1,0)
        self.keys.addWidget(self.api_secret, 1, 1)
        self.keys.addWidget(QLabel("Region"),2,0)
        self.keys.addWidget(self.region, 2, 1)


        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_to_file)

        self.mainLayout.addLayout(self.keys)
        self.mainLayout.addWidget(self.pem)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def save_to_file(self):
        #self.settings.setParam('ec2_id',self.ec2_id.text())
        self.settings.setParam('aws_access_key_id', re.sub("\n$","", self.api_access.text()) )
        self.settings.setParam('aws_secret_access_key', re.sub("\n$","",self.api_secret.text()) )
        self.settings.setParam('region', self.region.text())
        self.settings.writeParams()
        #try:
        #    os.mkdir(home+'/.aws',mode=0o700)
        #except:
        #    pass
        #with open(home+'/.aws/config','w+') as f:
        #    f.write('[default]\n')
        #    f.write('region = '+self.region.text()+'\n')
        #    f.write('output = json\n')
        #os.chmod(home+'/.aws/config',0o600)

        #with open(home+'/.aws/credentials','w+') as f:
        #    f.write('[default]\n')
        #    f.write('aws_access_key_id = '+self.api_access.text()+'\n')
        #    f.write('aws_secret_access_key = ' + self.api_secret.text() + '\n')
        #os.chmod(home+'/.aws/credentials',0o600)
        self.close()

    def fn_pem(self):
        file = QFileDialog()
        file.exec_()
        with  open(file.selectedFiles()[0],"r") as f:
            key = f.readlines()
        self.settings.setParam("pem", "".join(key))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IdsForm(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





