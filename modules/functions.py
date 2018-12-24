import re
import os
import sys
import paramiko
from os.path import expanduser
from io import StringIO
from PySide2.QtWidgets import *
from modules import SettingsManager

def tagsToDict(tags):
    return({x["Key"]: x["Value"] for x in tags})

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    path = os.path.join(base_path, relative_path)
    return(path)

def setNxXML(ip):
    settings = SettingsManager.settingsManager()
    user = settings.getParam("user")
    home = expanduser("~")

    with open(resource_path(os.path.join('files', 'sessions')),'r') as nx:
        nxs = nx.readlines()

    nxs = [re.sub('@ip@',ip,x) for x in nxs ]
    nxs = [re.sub('@user@', user, x) for x in nxs]
    #nxs = [re.sub('@export@', home, x) for x in nxs]

    nx_path = os.path.join(home,'.sessions')

    with open(nx_path,'w+') as nx:
        nx.writelines(nxs)

    return nx_path

def run_script(script):
    settings = SettingsManager.settingsManager()
    session = settings.getSession()
    ec2 = session.resource("ec2")
    instance = ec2.Instance(id = settings.getParam("ec2_id"))
    if instance.state["Name"] == "running":

        print("Conectando")
        key_string = StringIO(settings.getParam("pem"))
        key = paramiko.RSAKey.from_private_key(key_string)
        ip = instance.network_interfaces_attribute[0]["Association"]["PublicDnsName"]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username="root", pkey=key)

        print("Ejecutando")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(script)
        print(ssh_stdout.readlines())
        print(ssh_stderr.readlines())
        msgBox = QMessageBox()
        msgBox.setText("Executed Correctly")
    else:
        msgBox = QMessageBox()
        msgBox.setText("Lab offline, nox excecuted")
    msgBox.exec_()

def sudo(cmd):
    sudo = resource_path("files\elevate.exe ")
    command = sudo + cmd
    print(command)
    os.system(command)
