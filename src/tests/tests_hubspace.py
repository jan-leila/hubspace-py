import json

from credentials import username, password
from hubspace import Hubspace

hubspace = Hubspace(username, password)

def runTests():
    print("devices:")
    print(json.dumps(hubspace.getDevicesInfo()))
    print("devices states:")
    print(json.dumps(hubspace.getDeviceStates()))
    print("devices tags:")
    print(json.dumps(hubspace.getDeviceTags()))
    print("devices attributes:")
    print(json.dumps(hubspace.getDeviceAttributes()))
    print("devices states tags attributes:")
    print(json.dumps(hubspace.getDevicesInfo([
        "state",
        "tags",
        "attributes",
    ])))
    print(hubspace.getDevices())

    print("conclave access:")
    print(hubspace.getConclaveAccess())

    print("\nmetadata:")
    print(json.dumps(hubspace.getMetadata()))

if __name__ == "__main__":
    runTests()
