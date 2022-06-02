import json

from credentials import username, password
from hubspace import Hubspace

hubspace = Hubspace(username, password)

def runTests():
    print("devices:")
    print(json.dumps(hubspace.getDeviceInfo()))
    print("devices states:")
    print(json.dumps(hubspace.getDeviceStates()))
    print("devices tags:")
    print(json.dumps(hubspace.getDeviceTags()))
    print("devices attributes:")
    print(json.dumps(hubspace.getDeviceAttributes()))
    print("devices states tags attributes:")
    print(json.dumps(hubspace.getDevices([
        "state",
        "tags",
        "attributes",
    ])))

    print("conclave access:")
    print(hubspace.getConclaveAccess())


    print("\nmetadata:")
    print(json.dumps(hubspace.getMetadata()))

if __name__ == "__main__":
    runTests()
