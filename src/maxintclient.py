'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''

from src.MaximoConnector import MaximoConnector
import json
import time


#maxcon = MaximoConnector(url="http://localhost:7001/maximo/oslc",apikey="7j0d5ib3uugbl3jjiefn4597i8sjppcrj1ucbd0r")
maxcon = MaximoConnector(url="http://localhost:7001/meaweb",apikey="7j0d5ib3uugbl3jjiefn4597i8sjppcrj1ucbd0r")

#print(maxcon.whoami(False,False))
#apikey = maxcon.regenerateApiKey()
#print(apikey)
ms1 = int(round(time.time() * 1000))

for y in range(50):
    asset_array = []
    for x in range(200):
        asset_data = {}
        asset_data["assetnum"]= "TYM" + str(y) + "_" + str(x)
        asset_data["siteid"]= "BEDFORD"
        asset_data["description"]= "hello " + asset_data["assetnum"]
        asset_array.append(asset_data)
    resp = maxcon.integration_json_post("EXTSYS1", "MXASSETInterface", asset_array)
ms2 = int(round(time.time() * 1000))
print("time="+str(ms2-ms1))
print(json.dumps(resp.json()))





