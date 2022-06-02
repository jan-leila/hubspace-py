from time import sleep
import random
from string import ascii_lowercase

from credentials import deviceID
from tests_hubspace import hubspace

device = hubspace.getDevice(deviceID)

def runTests():
    print("default id:")
    print(device.getID())
    print("default info:")
    print(device.getInfo())
    print("default state:")
    print(device.getState())
    print("default tags:")
    print(device.getTags())
    print("default attributes:")
    print(device.getAttributes())
    print("default metadata:")
    print(device.getMetadata())
    print("default default name:")
    print(device.getDefaultName())
    print("default manufacturer name:")
    print(device.getManufacturerName())
    print("default model:")
    print(device.getModel())
    print("device class:")
    print(device.getDeviceClass())

    print("device name:")
    old_name = device.getName()
    print(old_name)
    new_name = ''.join(random.choice(ascii_lowercase) for i in range(10))
    print("setting device name to " + new_name + ":")
    print(device.setName(new_name))

    sleep(5)
    print("new device name:")
    print(device.getName())
    print("reseting device name:")
    print(device.setName(old_name))

    print("action 1 state:")
    action = device.readAction(1)
    print(action)

if __name__ == "__main__":
    runTests()
