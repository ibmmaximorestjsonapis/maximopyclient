'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''

#from mxconnector.WhereClause import WhereClause
#from mxconnector.MaximoConnector import MaximoConnector
#from mxconnector.selectclause import SelectClause

import mxconnector
import json
import time


maxcon = mxconnector.MaximoConnector(url="http://vmmxperf1.fyre.ibm.com:9080/maximo/oslc", apikey="1m34e43s71t2hm5pust15kr5lpf1l1prd7289a6q")
#maxcon = MaximoConnector(url="http://vmmxperf1.fyre.ibm.com:9080/maximo/oslc",user="wilson", password="wilson")

#print(maxcon.whoami(False,False))
#apikey = maxcon.regenerate_apikey()
#print(apikey)
ms1 = int(round(time.time() * 1000))
asset_set = maxcon.os_resource("OSLCASSET")
props2 = ["assetuid","assetid","orgid","siteid","assetnum","description","status","itemnum","itemtype","itemsetid","parent","assetlongdesc"]
props = ["assetnum","status","location","description"]
select_clause = mxconnector.SelectClause(props=props2)

resp = asset_set.fetch_first_page(select_clause=select_clause, stream=False, stable=False)
ms2 = int(round(time.time() * 1000))
print("time="+str(ms2-ms1))
print(json.dumps(resp))


where_filter = mxconnector.WhereClause()
where_filter.op_mode_or(True)
where_filter.op_in("status", ["APPR", "WAPPR"])
where_filter.op_in("priority", [1, 2])
print(where_filter.params())





