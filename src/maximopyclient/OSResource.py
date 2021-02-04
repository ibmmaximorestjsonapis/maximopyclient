'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''


class OSResource:

    def __init__(self, name, conn):
        self.name = name
        self.conn = conn
        self.ctx = "/os/"
        self.next_page_uri = None

    def fetch_resource(self, uri, select_clause, stream=False):
        if stream:
            self.ctx = "/stream/"
        else:
            self.ctx = "/os/"

        params = {}
        if select_clause is not None:
            select_clause.params().update(params)
        if uri is not None:
            self.conn.do_get(uri, params=params, headers=self.header_params)
        else:
            uri = self.conn.url+self.ctx+self.name.lower()
            self.conn.do_get(uri, params=params, headers=self.header_params)

    def fetch_all(self, where_clause=None, select_clause=None, uri=None, params=None, data_format="JSON", stream=False):
        if stream:
            self.ctx = "/stream/"
        else:
            self.ctx = "/os/"

        if params is None:
            params = {}
        params["ignorecollectionref"] = "1"
        if data_format== "CSV" or data_format == "XML":
            params["_format"] = data_format
        if where_clause is not None:
            params.update(where_clause.params())
        if select_clause is not None:
            params.update(select_clause.params())
        resp = None
        if uri is not None:
            resp = self.conn.do_get(uri, params=params)
        else:
            uri = self.conn.url+self.ctx+self.name.lower()
            resp = self.conn.do_get(uri, params=params)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        if data_format.lower() == "json":
            return resp.json()
        else:
            return resp.text()

    def fetch_first_page(self, where_clause=None, uri=None, select_clause=None, page_size=1000, stable=True, stream=False):

        if stream:
            self.ctx = "/stream/"
        else:
            self.ctx = "/os/"

        if stable == True and self.conn.session == False:
            raise Exception("stable paging not supported without session")

        params = {'oslc.pageSize': page_size,'ignorecollectionref': '1'}
        if where_clause is not None:
            params.update(where_clause.params())
        if select_clause is not None:
            params.update(select_clause.params())
        if stable:
            params['stablepaging'] = '1'
        if uri is not None:
            resp = self.conn.do_get(uri, params=params)
        else:
            uri = self.conn.url+self.ctx+self.name.lower()
            resp = self.conn.do_get(uri, params=params)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        self.conn.session = resp.cookies['JSESSIONID']
        resp_data = resp.json()
        if 'nextPage' in resp_data['responseInfo']:
            self.next_page_uri = resp_data['responseInfo']['nextPage']['href']
        return resp_data

    def has_next_page(self):
        return self.next_page_uri is not None

    def fetch_next_page(self):
        if self.next_page_uri is not None:
            resp = self.conn.do_get(self.next_page_uri)
            if resp.status_code>=400:
                raise Exception(resp.json()["Error"]["message"])
            resp_data = resp.json()
            self.next_page_uri = None
            if 'nextPage' in resp_data['responseInfo']:
                self.next_page_uri = resp_data['responseInfo']['nextPage']['href']

            return resp_data
        else:
            raise Exception("no next page")

    def create(self, json_data, uri=None, select_clause=None):
        if uri is None:
            uri = self.conn.url+self.ctx+self.name.lower()
        headers = {}
        if select_clause is not None:
            headers["properties"] = select_clause.to_string()

        resp = self.conn.do_post(uri, params={}, headers=headers, data=json_data)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        if select_clause is not None:
            return resp.json()
        else:
            return resp.headers['location']

    def replace(self, json_data, uri, select_clause=None):
        if uri is None:
            uri = json_data['href']
            if uri is None:
                raise Exception("missing uri")

        headers={}
        if select_clause is not None:
            headers['properties'] = select_clause.to_string()
        headers['x-method-override'] = 'PATCH'
        resp = self.conn.do_post(uri, params={}, headers=headers, data=json_data)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.json()

    def merge(self, json_data, uri=None, select_clause=None):
        if uri is None:
            uri = json_data['href']
            if uri is None:
                raise Exception("missing uri")
        headers={}
        if select_clause is not None:
            headers['properties'] = select_clause.to_string()

        headers['x-method-override']='PATCH'
        headers['patchtype'] = 'MERGE'
        headers['content-type'] = 'application/json'
        resp = self.conn.do_post(uri, params={}, headers=headers, data=json_data)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        elif resp.status_code == 200:
            return resp.json()

    def sync(self, json_data, uri=None, select_clause=None):
        if uri is None:
            uri = self.conn.url+"/os/"+self.name.lower()
        headers = {'x-method-override': 'SYNC'}
        if select_clause is not None:
            headers['properties'] = select_clause.to_string()
        resp = self.conn.do_post(uri, params={}, headers=headers, data=json_data)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.json()

    def delete(self, uri):
        if uri is None:
            raise Exception("missing uri")
        headers = {'x-method-override': 'DELETE'}
        resp = self.conn.do_post(uri, params={}, headers=headers)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        return resp

    def bulk(self, json_data, uri=None, select_clause=None):
        if uri is None:
            raise Exception("missing uri")
        headers = {}
        if select_clause is not None:
            headers['properties'] = select_clause.to_string()
        headers['x-method-override'] = 'BULK'
        resp = self.conn.do_post(uri, params={}, headers=headers, data=json_data)
        if resp.status_code>=400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.json()

    def sys_get_action(self, action_name, uri=None, params=None):
        if uri is None:
            uri = self.conn.url+"/os/"+self.name.lower()
        headers = {}
        params = {'action': action_name}
        resp = self.conn.do_get(uri, params=params, headers=headers)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.text()

    def sys_post_action(self, action_name, data=None, uri=None, params=None):
        if uri is None:
            uri = self.conn.url+"/os/"+self.name.lower()
        headers = {}
        params = {'action': action_name}
        resp = self.conn.do_post(uri, params=params, headers=headers, data=data)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.text()

    def invoke_method(self, action_name, data=None, uri=None, params=None):
        if uri is None:
            # uri = self.conn.url+"/os/"+self.name.lower()
            uri = data['href']
        headers = {'x-method-override': 'PATCH', 'patchtype': 'MERGE', 'content-type': 'application/json'}

        action = 'wsmethod:'+str(action_name)
        params = {'action': action}
        resp = self.conn.do_post(uri, params=params, headers=headers, data=data)

        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        if resp.json is not None:
            return resp.json()
        return resp

    def new(self, uri=None, select_clause=None):
        if uri is None:
            uri = self.conn.url+"/os/"+self.name.lower()
        headers = {}

        if select_clause is not None:
            headers['properties'] = select_clause.to_string()

        params = {'action': "new"}
        resp = self.conn.do_get(uri, params=params, headers=headers)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.json()

    def duplicate(self, uri, select_clause=None):
        if uri is None:
            raise Exception("missing uri")
        headers = {}

        if select_clause is not None:
            headers['properties'] = select_clause.to_string()

        params = {'action': "duplicate"}
        resp = self.conn.do_get(uri, params=params, headers=headers)
        if resp.status_code >= 400:
            raise Exception(resp.json()["Error"]["message"])
        return resp.json()
