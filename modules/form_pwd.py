#echo s3fs#$BUCKET /mnt/$BUCKET fuse _netdev,uid=userbda,gid=analytics,allow_other,umask=002,endpoint=us-east-2 0 0 >> /etc/fstab

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:33:56 2018

@author: dfischer
"""

from PySide2.QtWidgets import *
from modules.functions import *
from modules import SettingsManager as sm, functions


class PwdForm(QDialog):
    def __init__(self,parent):
        super(PwdForm,self).__init__(parent)
        self.settings = sm.settingsManager()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("Password Setup")

        self.mainLayout = QVBoxLayout()

        self.pwd = QLineEdit()
        self.pwd.setEchoMode(QLineEdit.Password)

        self.save = QPushButton("save")
        self.save.clicked.connect(self.fn_save)

        self.mainLayout.addWidget(self.pwd)
        self.mainLayout.addWidget(self.save)

        self.setLayout(self.mainLayout)

    def fn_save(self):
        settings = SettingsManager.settingsManager()
        user = settings.getParam("user")
        cmd = 'echo "{}:{}" | sudo chpasswd'.format(user,self.pwd.text())
        print(cmd)
        functions.run_script(cmd)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PwdForm(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





