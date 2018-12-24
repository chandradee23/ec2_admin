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


class BucketForm(QDialog):
    def __init__(self,parent):
        super(BucketForm,self).__init__(parent)
        self.settings = sm.settingsManager()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setWindowTitle("Bucket Connector")

        self.api_access = self.settings.getParam('aws_access_key_id')
        self.api_secret = self.settings.getParam('aws_secret_access_key')
        self.region = self.settings.getParam('region')
        self.user = self.settings.getParam("user")

        self.mainLayout = QVBoxLayout()

        self.session = self.settings.getSession()
        s3 = self.session.resource("s3")
        self.buckets = {x.name: x for x in list(s3.buckets.all())}

        self.combo_bucket = QComboBox()
        self.combo_bucket.addItems(list(self.buckets.keys()))

        self.connect = QPushButton("Connect")
        self.connect.clicked.connect(self.fm_connect)

        self.mainLayout.addWidget(self.combo_bucket)
        self.mainLayout.addWidget(self.connect)

        self.setLayout(self.mainLayout)

    def fm_connect(self):
        settings = SettingsManager.settingsManager()
        cmd_limpiar = 'cat /etc/fstab | grep -v {} > /etc/fstab.tmp;'.format(self.combo_bucket.currentText())
        cmd_move = 'mv /etc/fstab.tmp /etc/fstab;'
        cmd_fstab = 'echo s3fs#{bucket} /home/{user}/{bucket} fuse ' \
                    '_netdev,uid={user},allow_other,umask=002,endpoint={region} 0 0 ' \
                    '>> /etc/fstab;'.format(bucket = self.combo_bucket.currentText(),
                                            region = self.region,
                                            user = self.user)
        cmd_api = 'echo '+self.api_access  + ':' + self.api_secret+' > /etc/passwd-s3fs;' \
                                                            'chmod 640 /etc/passwd-s3fs;'
        cmd_mount = 'mkdir /home/{user}/{bucket};mount /home/{user}/{bucket}'.format(bucket =self.combo_bucket.currentText(),
                                                                                     user = self.user)
        cmd = cmd_limpiar +cmd_move + cmd_fstab + cmd_api + cmd_mount
        print(cmd)
        functions.run_script(cmd)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BucketForm(None)
    window.show()
# sys.exit(app.exec_())
    app.exec_()





