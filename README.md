# hubspace-py

https://pypi.org/project/hubspace/1.0.0/

tools for intergrading with hubspace though python

### installing:
`pip install hubspace`

### getting started:

```py
from hubspace import Hubspace

hubspace = Hubspace(username, password)
```

### examples:

```py
# get json info for all devices
hubspace.getDeviceInfo()
# get array of all device objects
devices = hubspace.getDevices()
# get target device object
device = hubspace.getDevice(deviceID)

# get additional information about devices
states = hubspace.getDeviceStates()
tags = hubspace.getDeviceTags()
attributes = hubspace.getDeviceAttributes()

# get all data for all devices
self.getDevices(["state", "tags", "attributes"])

# get device metadata
hubspace.getMetadata()
# get conclave access information
hubspace.getConclaveAccess()

# get the id of this device
device.getID()
# get the hubspace that created this device
device.getHubspace()
# get the info for this device
device.getInfo()
# get additional information about this device
device.getState()
device.getTags()
device.getAttributes()
# get metadata for this device
device.getMetadata()
# get the name of this device
device.getName()
# set the name of this device
device.setName()
# get the default name for this device
device.getDefaultName()
# get the name of the manufacturer of this device
device.getManufacturerName()
# get the model number for this device
device.getModel()
# get the class of the device (ie. light, fan ...etc)
device.getDeviceClass()
# read an action type for this device (see getgetAttributes for action info)
device.readAction(actionID)
# write action data for this device
device.writeAction(actionID, actionData)
```