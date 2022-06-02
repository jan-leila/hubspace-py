from time import time, sleep

from credentials import username, password
from hubspace.hubspace_user import HubspaceUser

user = HubspaceUser(username, password)

def runTests():
    print("testing credentials:")
    print(user.testCredentials())

    print("account info:")
    print(user.getInfo())

    print("account id:")
    print(user.getAccountID())
    print("credential id:")
    print(user.getCredentialID())
    print("first name:")
    print(user.getFirstName())
    print("last name:")
    print(user.getLastName())

    timeLeft = user.getCredentialExperation() - time()
    
    ranLoop = False
    while timeLeft > 0:
        print("waiting for credentials to expire: " + "{:.6f}".format(max(timeLeft, 0)) + " seconds remaining    ", end="\r", flush=True)
        timeLeft = user.getCredentialExperation() - time() + 5
        ranLoop = True
        sleep(0.1)
    if ranLoop:
        print(" " * 67)
    print("testing credentials:")
    print(user.testCredentials())

if __name__ == "__main__":
    runTests()
