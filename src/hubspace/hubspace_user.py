from email import header
import os
import re
import hashlib
import base64
import requests
import datetime
import json

_default_duration = 120 * 1000
_default_expiration_buffer = 10 * 1000

def _getTokenBody(token):
    body_base64 = token.split(".")[1]
    body_base64 = body_base64 + ("=" * (4 - len(body_base64) % 4))
    body_text = base64.b64decode(body_base64).decode('utf-8')
    return json.loads(body_text)

def _getRefreshToken(username, password):
    code_verifier = re.sub('[^a-zA-Z0-9]+', '',base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8'))
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').replace('=', '')

    with requests.get(url = "https://accounts.hubspaceconnect.com/auth/realms/thd/protocol/openid-connect/auth", params = {
        'response_type':         'code',
        'client_id':             'hubspace_android',
        'redirect_uri':          'hubspace-app://loginredirect',
        'code_challenge':        code_challenge,
        'code_challenge_method': 'S256',
        'scope':                 'openid offline_access',
    }) as r:
        session_code = re.search('session_code=(.+?)&', r.text).group(1)
        execution = re.search('execution=(.+?)&', r.text).group(1)
        tab_id = re.search('tab_id=(.+?)&', r.text).group(1)
        cookie = r.cookies.get_dict()

    with requests.post(
        "https://accounts.hubspaceconnect.com/auth/realms/thd/login-actions/authenticate?session_code="+ session_code + "&execution=" + execution + "&client_id=hubspace_android&tab_id=" + tab_id,
        data={        
            "username":     username,
            "password":     password,
            "credentialId": "", 
        },
        headers={
            "Content-Type":    "application/x-www-form-urlencoded",
            "accept-encoding": "gzip",
        },
        cookies=cookie,
        allow_redirects = False
    ) as r:
        location = r.headers.get('location')
        code = re.search('&code=(.+?)$', location).group(1)

    with requests.post(
        "https://accounts.hubspaceconnect.com/auth/realms/thd/protocol/openid-connect/token",
        data={        
            "grant_type":    "authorization_code",
            "code":          code ,
            "redirect_uri" : "hubspace-app://loginredirect",
            "code_verifier": code_verifier,
            "client_id":     "hubspace_android",
        },
        headers={
            "Content-Type":    "application/x-www-form-urlencoded",
            "accept-encoding": "gzip",
        },
    ) as r:
        return r.json().get('refresh_token')

class HubspaceUser:

    _api = "https://api2.afero.net/v1/"

    _refresh_token = None

    _access_token = None
    _access_token_exp = 0

    _accountID = None

    def __init__(self, username=None, password=None, token=None, token_duration=_default_duration, _expiration_buffer=_default_expiration_buffer):
        self._username = username
        self._password = password
        self._refresh_token = token
        self._token_duration = token_duration
        self._expiration_buffer = _expiration_buffer

    def _getRefreshToken(self):
        if self._refresh_token == None:
            self._refresh_token = _getRefreshToken(self._username, self._password)
        return self._refresh_token

    def _getAccessToken(self):

        now = datetime.datetime.now().timestamp()

        if self._access_token == None or self._access_token_exp - self._expiration_buffer >= now:
            with requests.post(
                "https://accounts.hubspaceconnect.com/auth/realms/thd/protocol/openid-connect/token",
                data={        
                    "client_id":     "hubspace_android",
                    "scope":         "openid email offline_access profile",
                    "grant_type":    "refresh_token",
                    "refresh_token": self._getRefreshToken(),
                },
                headers={
                    "Content-Type":    "application/x-www-form-urlencoded",
                    "accept-encoding": "gzip",
                },
            ) as r:
                self._access_token = r.json().get('id_token')
                body = _getTokenBody(self._access_token)
                if not body["exp"] == None:
                    self._access_token_exp = body["exp"]
                elif not body["iat"] == None:
                    self._access_token_exp = body["exp"] + self._token_duration
                else:
                    self._access_token_exp = now + self._token_duration
        return self._access_token

    def _getAuthorization(self):
        return "Bearer " + self._getAccessToken()
        
    def exportCredentials(self):
        return self._getRefreshToken()
    
    def testCredentials(self):
        try:
            if not self._getAccessToken() == None:
                return True
        except:
            return False

    def getCredentialExperation(self):
        return self._access_token_exp 

    def _getHeaders(self, host):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "accept-encoding": "gzip",
            "authorization": self._getAuthorization(),
        }

        if not host == None:
            headers["host"] = host

        return headers
    
    def get(self, path="", data=None, host=None):
        with requests.get(
            url=self._api + path,
            headers=self._getHeaders(host),
            data=data
        ) as r:
            return r.json()

    def post(self, path="", data=None, host=None):
        with requests.post(
            url=self._api + path,
            headers=self._getHeaders(host),
            data=data
        ) as r:
            return r.json()

    def put(self, path="", data=None, host=None):
        with requests.put(
            url=self._api + path,
            headers=self._getHeaders(host),
            data=data
        ) as r:
            return r.json()

    def getInfo(self):
        return self.get("users/me")

    def getAccountID(self):
        if self._accountID == None:
            self._accountID = self.getInfo()['accountAccess'][0]['account']['accountId']
        return self._accountID

    def getCredentialID(self):
        self._accountID = self.getInfo()['credential']['credentialId']

    def getFirstName(self):
        self._accountID = self.getInfo().get('firstName')

    def getLastName(self):
        self._accountID = self.getInfo().get('lastName')
