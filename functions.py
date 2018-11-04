import re
import os
import sys

config_filename = os.path.join(os.path.expanduser('~')) + "/.config_aws_ec2.cfg"

def loadIDS():
    print(config_filename)
    try:
        reader = open(config_filename)
        keys = {
            "user" : re.sub("\n|\r", "", reader.readline()),
            "password" : re.sub("\n|\r", "", reader.readline()),
            "region" : re.sub("\n|\r", "", reader.readline())
        }
        reader.close()
        return(keys)
    except:
        return(None)

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