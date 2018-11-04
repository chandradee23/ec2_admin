import re
import os

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