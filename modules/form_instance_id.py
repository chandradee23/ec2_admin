#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from modules.functions import *
from modules import SettingsManager as sm, functions as fn
import os

home = os.path.expanduser("~")

class idEc2Form(QDialog):
    def __init__(self,parent):
        super(idEc2Form,self).__init__(parent)
        self.settings = sm.settingsManager()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("AWS API Manager")

        try:
            con = self.settings.getSession()
            ec2 = con.resource("ec2", use_ssl = False)
            instances = list(ec2.instances.all())
        except:
            pass

        dict = {fn.tagsToDict(i.tags)["Name"] :  i.id for i in instances}

        self.combo_ec2 = QComboBox()
        for i in sorted(dict.keys()):
            self.combo_ec2.addItem(i,dict[i])


        self.mainLayout = QVBoxLayout()

        self.keys = QGridLayout()
        self.keys.addWidget(QLabel("EC2 Lab Name"),0,0)
        self.keys.addWidget(self.combo_ec2, 0, 1)


        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_to_file)

        self.mainLayout.addLayout(self.keys)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def save_to_file(self):
        id = self.combo_ec2.currentData()
        print(self.combo_ec2.currentData())
        self.settings.setParam('ec2_id',id)
        self.settings.writeParams()
        self.parent.parent.getKeys()

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = idEc2Form(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





