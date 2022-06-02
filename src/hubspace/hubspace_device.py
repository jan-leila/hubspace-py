import json

from .util import getExpansions

class HubspaceDevice:

    _defaultName = None
    _manufacturerName = None
    _model = None
    _deviceClass = None

    def __init__(self, hubspace, deviceID):
        self._hubspace = hubspace
        self._deviceID = deviceID
    
    def getID(self):
        return self._deviceID

    def getHubspace(self):
        return self._hubspace

    def getInfo(self, expansions=[]):
        return self._hubspace.get("accounts/" + self._hubspace.getAccountID() + "/devices/" + self._deviceID + getExpansions(expansions))
    
    def getState(self):
        return self.getInfo(["state"])["deviceState"]

    def getTags(self):
        return self.getInfo(["tags"])["deviceTags"]

    def getAttributes(self):
        return self.getInfo(["attributes"])["attributes"]
    
    def _executeAction(self, actionType, attributeID, data):
        return self._hubspace.post(
            "accounts/" + self._hubspace.getAccountID() + "/devices/" + self._deviceID + "/actions",
            json.dumps({
                "type": actionType,
                "attrId": attributeID,
                "data": data,
            }),
        )

    def getMetadata(self):
        metadata = self._hubspace.getMetadata()
        for device in metadata:
            deviceID = device.get("deviceId")
            if deviceID == self._deviceID:
                info = device["description"]["device"]

                self._defaultName = info["defaultName"]
                self._manufacturerName = info["manufacturerName"]
                self._model = info["model"]
                self._deviceClass = info["deviceClass"]

                return device
    
    def getName(self):
        return self.getInfo()["friendlyName"]

    def getDefaultName(self):
        if self._defaultName == None:
            self.getMetadata()
        return self._defaultName

    def getManufacturerName(self):
        if self._manufacturerName == None:
            self.getMetadata()
        return self._manufacturerName

    def getModel(self):
        if self._model == None:
            self.getMetadata()
        return self._model

    def getDeviceClass(self):
        if self._deviceClass == None:
            self.getMetadata()
        return self._deviceClass

    def readAction(self, attributeID):
        return self._executeAction("attribute_read", attributeID, "")

    def writeAction(self, attributeID, data):
        return self._executeAction("attribute_write", attributeID, data)

    def setName(self, name):
        return self._hubspace.put(
            "accounts/" + self._hubspace.getAccountID() + "/devices/" + self._deviceID + "/friendlyName",
            json.dumps({
                "friendlyName": name,
            }),
        )
