import json
from os.path import expanduser
import boto3

home = expanduser("~")

settings_path = home+'/.aws_keys.json'

class settingsManager():

    def __init__(self):
        try:
            with open(settings_path, 'r') as f:
                self.params = json.load(f)
        except:
            with open(settings_path, 'w+') as f:
                f.writelines(["{}"])
            with open(settings_path, 'r') as f:
                self.params = json.load(f)

    def setParam(self, key, value):
        self.params[key] = str(value)

    def writeParams(self):
        with open(settings_path, 'w') as f:
            json.dump(self.params,f)

    def refresh(self):
        self = settingsManager()

    def getParam(self,key):
        try:
            return(self.params[key])
        except:
            return("")

    def getSession(self):
        try:
            session = boto3.Session(
                aws_access_key_id = self.getParam("aws_access_key_id"),
                aws_secret_access_key = self.getParam("aws_secret_access_key"),
                region_name=self.getParam("region")
            )
            return session
        except:
            print('cant connect aws')
            return None
