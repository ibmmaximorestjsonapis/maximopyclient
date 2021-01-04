'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''


import requests
import json
from src.OSResource import OSResource
from src.service import Service
import base64


class MaximoConnector:
    
    def __init__(self, url, apikey=None, user=None, password=None, session=False):
        self.url = url
        self.apikey = apikey
        self.query_params = {}
        self.header_params = {}
        self.session = session
        #self.sessionid = None
        if apikey is not None:
            self.header_params['apikey'] = apikey
            if session==True:
                self.query_params['enablesession'] = "1"
        elif user is not None and password is not None:
            maxauth = user+":"+password
            maxauth_bytes = maxauth.encode('utf-8')
            base64_bytes = base64.b64encode(maxauth_bytes)
            base64_maxauth = base64_bytes.decode('utf-8')
            self.header_params['maxauth'] = base64_maxauth
            self.session = True
        
        self.query_params['lean'] = "1"
    
    def integration_json_post(self, extSysName, interfaceName, data):
        uri = self.url+"/esqueue/"+extSysName+"/"+interfaceName
        print(uri)
        print( json.dumps(data))
        self.header_params["content-type"] = "application/json"
        resp = requests.post(uri, params=self.query_params, headers=self.header_params, json=data, cookies=None)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        return resp

    def do_post(self, uri, data, params=None, headers=None, cookies=None):
        if headers is None:
            headers = self.header_params
        else:
            headers.update(self.header_params)
        if params is None:
            params = self.query_params
        else:
            params.update(self.query_params)
        for k in params:
            print(k+"="+params[k])
        if self.sessionid is not None:
            if cookies is None:
                cookies = {}
            cookies['JSESSIONID'] = self.sessionid
        resp = requests.post(uri, params=params, headers=headers, data=data, cookies=cookies)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        return resp
    
    def do_get(self, uri, params=None, headers=None, cookies=None):
        if headers is None:
            headers = self.header_params
        else:
            headers.update(self.header_params)
        
        if params is None:
            params = self.query_params
        else:
            params.update(self.query_params)
        for k in params:
            print(k+"="+str(params[k]))
        print((params['oslc.pageSize']))
        resp = requests.get(uri, params=params, headers=headers)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        return resp

    
    def os_resource(self, osName):
        return OSResource(osName, self)  
    
    def service_resource(self, serviceName):
        return Service(serviceName, self)    
  
    
    def whoami(self, addApps, wcsyscfg):
        if addApps==True:
            self.query_params["addapps"] = "1"
        elif wcsyscfg==True:
            self.query_params["wcsyscfg"] = "1"
        tgt_uri = self.url+"/whoami"
        return self.do_get(tgt_uri).json()
    
    def system_info(self):
        tgt_uri = self.url+"/systeminfo"
        return self.do_get(tgt_uri).json()

    def license_info(self):
        tgt_uri = self.url+"/license"
        resp = self.do_get(tgt_uri)
        return resp.json()
    
    def mmi_this_server(self):
        tgt_uri = self.url+"/members/thisserver"
        resp = self.do_get(tgt_uri)
        return resp.json()

    def ping(self):
        tgt_uri = self.url+"/ping"
        resp = self.do_get(tgt_uri)
        return resp.json()
    
    def images(self, uri):
        tgt_uri = self.url+"/ping"
        resp = self.do_get(tgt_uri)
        return resp.json()

    def regenerate_apikey(self, expiration=-1):
        tgt_uri = self.url+"/apitoken/create"
        data = {}
        data['expiration'] = expiration
        resp = self.do_post(tgt_uri, data=json.dumps(data))
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        apikey = resp.json()["apikey"]
        self.header_params['apikey'] = apikey
        return apikey

    
    def revoke_apikey(self):
        tgt_uri = self.url+"/apitoken/revoke"
        self.do_post(tgt_uri)
