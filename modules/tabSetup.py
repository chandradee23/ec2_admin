
from PySide2.QtWidgets import *
from modules.form_apps import appsForm
from modules.form_aws_keys import IdsForm
from modules.form_bucket import  BucketForm
from modules.form_pwd import  PwdForm
from modules.form_instance_id import idEc2Form
from modules.form_user import userForm
from modules import functions as fn

class tabSetup(QWidget):

    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        layout = QVBoxLayout()

        choco = QPushButton('Install Chocolatelly')
        choco.clicked.connect(self.fn_choco)

        apps = QPushButton('Install Apps')
        apps.clicked.connect(self.fn_apps)

        saveid = QPushButton('Set Keys')
        saveid.clicked.connect(self.fn_saveid)

        ec2 = QPushButton('Select EC2')
        ec2.clicked.connect(self.fn_set_ec2)

        useradd = QPushButton("Create User on EC2")
        useradd.clicked.connect(self.fn_useradd)

        pwd = QPushButton('Set Password for user')
        pwd.clicked.connect(self.fn_set_pwd)

        add_bucket = QPushButton("Mount Bucket to EC2")
        add_bucket.clicked.connect(self.fn_add_bucket)

        layout.addWidget(choco)
        layout.addWidget(apps)
        layout.addWidget(saveid)
        layout.addWidget(ec2)
        layout.addWidget(useradd)
        layout.addWidget(pwd)
        layout.addWidget(add_bucket)
        self.setLayout(layout)

    def fn_choco(self):
        fn.sudo("\"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe\" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command \"iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))\" && SET \"PATH=%PATH%;%ALLUSERSPROFILE%\\chocolatey\\bin\"")

    def fn_apps(self):
        win = appsForm(self)
        win.exec()

    def fn_saveid(self):
        win = IdsForm(self)
        win.exec()
        self.parent.getKeys()

    def fn_add_bucket(self):
        win = BucketForm(self)
        win.exec()

    def fn_set_pwd(self):
        win = PwdForm(self)
        win.exec()

    def fn_set_ec2(self):
        win = idEc2Form(self)
        win.exec()

    def fn_useradd(self):
        win = userForm(self)
        win.exec()

