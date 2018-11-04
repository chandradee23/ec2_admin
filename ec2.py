#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import boto3
import time
import os
import sys
from ec2_ids import IdsForm, loadIDS
from functions import *

scriptDir = os.path.dirname(sys.executable)
config_filename = os.path.join(os.path.expanduser('~')) + "/.config_aws_ec2.cfg"


class mainWindow(QMainWindow):
    def __init__(self, parent):
        super(mainWindow, self).__init__(parent)

        self.setMinimumWidth(400)
        self.setWindowTitle("AWS EC2 Manager")
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'ec2.png'))

        self.setCentralWidget(mainWidget(self))


class mainWidget(QWidget):
    def __init__(self, parent):
        super(mainWidget, self).__init__(parent)

        # Acciones
        self.hbox_manipulate = QHBoxLayout()
        self.hbox_manipulate.addWidget(QLabel("Actions:"))

        self.on = QPushButton("Turn On")
        self.off = QPushButton("Turn Off")
        self.saveid = QPushButton("Set IDs")

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
        self.grid_attr.addWidget(QLabel('Name'), 0, 0)
        self.name = QLineEdit()
        self.name.setReadOnly(True)
        self.grid_attr.addWidget(self.name, 0, 1)

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
        self.vbox.addLayout(self.hbox_manipulate)
        self.vbox.addLayout(self.grid_manipulate)
        self.vbox.addLayout(self.hbox_attr)
        self.vbox.addLayout(self.grid_attr)
        self.vbox.addWidget(self.refresh)
        self.vbox.addLayout(self.hbox_serv)
        self.vbox.addLayout(self.hbox_url)

        self.setLayout(self.vbox)
        self.getKeys()
        # self.fn_status()

        self.show()

    def getKeys(self):
        self.keys = loadIDS()

        self.user = self.keys["user"]
        self.password = self.keys["password"]
        self.region = self.keys["region"]
        self.id_ec2 = self.keys["id_ec2"]

        try:
            self.session = boto3.Session(
                aws_access_key_id=self.user,
                aws_secret_access_key=self.password,
                region_name=self.region
            )
            self.ec2 = self.session.resource("ec2")
            self.i = self.ec2.Instance(id=self.id_ec2)
            self.fn_status()
        except:
            pass

    def fn_status(self):
        try:
            state = self.i.state["Name"]
            self.status.setText(state)
            self.instance_type.setCurrentText(self.i.instance_type)
            tags = {x["Key"]: x["Value"] for x in self.i.tags}
            # print(tags)
            self.name.setText(tags["Name"])
        except:
            self.name.setText("Invalid ID")
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

    def fn_set_type(self):
        if (self.i.state["Name"] == "stopped"):
            self.i.modify_attribute(Attribute='instanceType', Value=self.instance_type.currentText())
        self.fn_status()

    def launch_kodex(self):
        QDesktopServices.openUrl(
            QUrl("http://" + self.i.network_interfaces_attribute[0]["Association"]["PublicDnsName"]))

    def launch_rstudio(self):
        QDesktopServices.openUrl(
            QUrl("http://" + self.i.network_interfaces_attribute[0]["Association"]["PublicDnsName"] + ":8080"))

    def launch_jupyter(self):
        QDesktopServices.openUrl(
            QUrl("http://" + self.i.network_interfaces_attribute[0]["Association"]["PublicDnsName"] + ":3000"))


class IdsForm(QDialog):
    def __init__(self, parent):
        super(IdsForm, self).__init__(parent)
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
        self.keys.addWidget(QLabel("Instance ID"), 0, 0)
        self.keys.addWidget(QLabel("API User"), 1, 0)
        self.keys.addWidget(QLabel("API Password"), 2, 0)
        self.keys.addWidget(QLabel("Region"), 3, 0)

        self.keys.addWidget(self.id, 0, 1)
        self.keys.addWidget(self.user, 1, 1)
        self.keys.addWidget(self.password, 2, 1)
        self.keys.addWidget(self.region, 3, 1)

        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_to_file)

        self.mainLayout.addLayout(self.keys)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def save_to_file(self):
        with open(config_filename, 'w+') as file:
            file.write(self.user.text() + "\n")
            file.write(self.password.text() + "\n")
            file.write(self.region.text() + "\n")
            file.write(self.id.text() + "\n")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow(None)
    window.show()
    # sys.exit(app.exec_())
    app.exec_()
