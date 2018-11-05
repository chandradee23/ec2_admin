#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from PySide2.QtGui import *
#from PySide2.QtCore import *
import boto3
import time
#import os
import sys
from ec2_ids import IdsForm, loadIDS
from functions import *

class mainWindow(QMainWindow):
    def __init__(self, parent):
        super(mainWindow, self).__init__(parent)

        self.setMinimumWidth(400)
        self.setWindowTitle("AWS EC2 Manager Admin")
        self.setWindowIcon(QIcon(resource_path(os.path.join('img','ec2.png') )))
        self.setCentralWidget(mainWidget(self))


class mainWidget(QWidget):
    def __init__(self, parent):
        super(mainWidget, self).__init__(parent)

        self.getKeys()

        self.hbox_instance = QHBoxLayout()
        self.instance_name = QComboBox()
        self.hbox_instance.addWidget(self.instance_name)
        self.active = QCheckBox("Activas")
        self.combo_instances()
        self.active.clicked.connect(self.combo_instances)
        self.hbox_instance.addWidget(self.active)
        self.instance_name.currentTextChanged.connect(self.fn_set_instance)

        # Acciones
        self.hbox_manipulate = QHBoxLayout()
        self.hbox_manipulate.addWidget(QLabel("Actions:"))

        self.on = QPushButton("Turn On")
        self.off = QPushButton("Turn Off")
        self.saveid = QPushButton("Set API")

        self.grid_manipulate = QGridLayout()
        self.grid_manipulate.addWidget(self.on, 0, 0)
        self.grid_manipulate.addWidget(self.off, 0, 1)
        self.grid_manipulate.addWidget(self.saveid, 0, 2)

        self.on.clicked.connect(self.fn_prender)
        self.off.clicked.connect(self.fn_apagar)
        self.saveid.clicked.connect(self.fn_saveid)

        # Tamaño
        self.grid_manipulate.addWidget(QLabel('Instance Size:'), 1, 0)
        self.instance_type = QComboBox()
        self.instance_type.addItems(["t2.nano",
                                     "t2.micro",
                                     "t2.small",
                                     "t2.medium",
                                     "t2.large",
                                     "t2.xlarge",
                                     "t2.2xlarge",
                                     "m4.large",
                                     "m4.xlarge",
                                     "m4.2xlarge",
                                     "m4.4xlarge",
                                     "m4.10xlarge",
                                     "m4.16xlarge",
                                     "c4.large",
                                     "c4.xlarge",
                                     "c4.2xlarge",
                                     "c4.4xlarge",
                                     "c4.8xlarge",
                                     "r4.large",
                                     "r4.xlarge",
                                     "r4.2xlarge",
                                     "r4.4xlarge",
                                     "r4.8xlarge",
                                     "r4.16xlarge"
                                     ])
        self.grid_manipulate.addWidget(self.instance_type, 1, 1)
        self.set_type = QPushButton("Set Size")
        self.grid_manipulate.addWidget(self.set_type, 1, 2)
        self.set_type.clicked.connect(self.fn_set_type)

        # Atributos
        self.hbox_attr = QHBoxLayout()
        self.hbox_attr.addWidget(QLabel("Instance Information:"))

        self.grid_attr = QGridLayout()
        self.grid_attr.addWidget(QLabel('ID'), 0, 0)
        self.ec2_id = QLineEdit()
        self.ec2_id.setReadOnly(True)
        self.grid_attr.addWidget(self.ec2_id, 0, 1)

        self.grid_attr.addWidget(QLabel('IP'), 1, 0)
        self.ip = QLineEdit()
        self.ip.setReadOnly(True)
        self.grid_attr.addWidget(self.ip, 1, 1)

        self.grid_attr.addWidget(QLabel('DNS'), 2, 0)
        self.dns = QLineEdit()
        self.dns.setReadOnly(True)
        self.grid_attr.addWidget(self.dns, 2, 1)

        self.grid_attr.addWidget(QLabel('Status'), 3, 0)
        self.status = QLineEdit()
        self.status.setReadOnly(True)
        self.grid_attr.addWidget(self.status, 3, 1)

        # Servicios
        self.hbox_serv = QHBoxLayout()
        self.hbox_serv.addWidget(QLabel("Launch Services:"))

        self.kodex = QPushButton("Kodexplorer")
        self.rstudio = QPushButton("RStudio")
        self.jupyter = QPushButton("Jupyter")

        self.hbox_url = QHBoxLayout()
        self.hbox_url.addWidget(self.kodex)
        self.hbox_url.addWidget(self.rstudio)
        self.hbox_url.addWidget(self.jupyter)

        self.kodex.clicked.connect(self.launch_kodex)
        self.rstudio.clicked.connect(self.launch_rstudio)
        self.jupyter.clicked.connect(self.launch_jupyter)

        self.refresh = QPushButton("Refresh")
        self.refresh.clicked.connect(self.fn_status)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_instance)
        self.vbox.addLayout(self.hbox_manipulate)
        self.vbox.addLayout(self.grid_manipulate)
        self.vbox.addLayout(self.hbox_attr)
        self.vbox.addLayout(self.grid_attr)
        self.vbox.addWidget(self.refresh)
        self.vbox.addLayout(self.hbox_serv)
        self.vbox.addLayout(self.hbox_url)

        self.setLayout(self.vbox)
        self.fn_set_instance()
        self.fn_status()

        self.show()

    def combo_instances(self):
        try:
            self.instances = [x for x in self.ec2.instances.all()]
            self.instance_name.clear()
            for i in self.instances:
                tags = tagsToDict(i.tags)
                if self.active.checkState() == 0 or i.state["Name"] == "running":
                    self.instance_name.addItem(tags["Name"], i)
        except:
            pass

    def fn_set_instance(self):
        self.i = self.instance_name.currentData()
        self.fn_status()

    def getKeys(self):
        try:
            self.keys = loadIDS()

            self.user = self.keys["user"]
            self.password = self.keys["password"]
            self.region = self.keys["region"]

            self.session = boto3.Session(
                aws_access_key_id=self.user,
                aws_secret_access_key=self.password,
                region_name=self.region
            )
            self.ec2 = self.session.resource("ec2")
        except:
            pass

    def fn_status(self):
        try:
            self.i.reload()
            state = self.i.state["Name"]
            self.status.setText(state)
            self.instance_type.setCurrentText(self.i.instance_type)
            tags = tagsToDict(self.i.tags)
            # print(tags)
            self.ec2_id.setText(self.i.id)
        except:
            self.ec2_id.setText("Invalid ID")
        try:
            self.ip.setText(self.i.network_interfaces_attribute[0]["Association"]["PublicIp"])
            self.dns.setText(self.i.network_interfaces_attribute[0]["Association"]["PublicDnsName"])
        except:
            self.ip.setText("")
            self.dns.setText("")

    def fn_prender(self):
        self.i.start()
        while self.i.state["Name"] != "running":
            print(".", end="")
            self.status.setText(self.i.state["Name"])
            time.sleep(2)
            self.i.reload()
        self.fn_status()

    def fn_apagar(self):
        self.i.stop()
        time.sleep(2)
        self.i.reload()
        self.status.setText(self.i.state["Name"])

    def fn_saveid(self):
        win = IdsForm(self)
        win.exec()
        self.getKeys()
        self.combo_instances()

    def fn_set_type(self):
        if (self.i.state["Name"] == "stopped"):
            self.i.modify_attribute(Attribute='instanceType', Value=self.instance_type.currentText())
        self.fn_status()

    def launch_kodex(self):
        QDesktopServices.openUrl("http://" + self.i.network_interfaces_attribute[0]["Association"]["PublicDnsName"])

    def launch_rstudio(self):
        QDesktopServices.openUrl("http://" + self.i.network_interfaces_attribute[0]["Association"]["PublicDnsName"] + ":8080")

    def launch_jupyter(self):
        QDesktopServices.openUrl("http://" + self.i.network_interfaces_attribute[0]["Association"]["PublicDnsName"] + ":3000")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow(None)
    window.show()
    # sys.exit(app.exec_())
    app.exec_()
