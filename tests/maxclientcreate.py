'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''


import maximopyclient
import json
import time


maxcon = maximopyclient.MaximoConnector(url="http://localhost:7001/maximo/api", apikey="n3i5idbad2omci5an3cnn7e5m4fmka29tr40t2h0", session=True)

wo_set = maxcon.os_resource('MXAPIWODETAIL')

select_clause = maximopyclient.SelectClause(['wonum'])

assets = ['AT100','AT101','AT102','AT103']

wo = {'siteid':'BEDFORD','worktype':'EM'}

for asset in assets:
    wo['assetnum'] = asset
    wo_resp = wo_set.create(wo,select_clause=select_clause)
    print("created workorder "+wo_resp['wonum'])



