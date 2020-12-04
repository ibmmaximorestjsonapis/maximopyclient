'''
Created on Aug 9, 2020

@author: AnamitraBhattacharyy
'''

class Service(object):
    '''
    classdocs
    '''


    def __init__(self, name, conn):
        self.name = name
        self.conn = conn
        self.uri = self.conn.uri+"/os/"+self.name.lower()
        
    def wsmethodGetAction(self, methodName, params=None):
        headers={}
        params={}
        params['action'] = "wsmethod:"+methodName 
        resp = self.conn.do_get(self.uri, params=params)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.text()

    def wsmethodPostAction(self, methodName, data=None, params=None):
        headers={}
        params={}
        params['action'] = "wsmethod:"+methodName  
        resp = self.conn.do_post(self.uri, params=params, headers=headers, data=data)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.text()
