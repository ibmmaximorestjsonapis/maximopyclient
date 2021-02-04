'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''

import maximopyclient

# Create a connector instance
maxcon = maximopyclient.MaximoConnector(url="http://localhost:7001/maximo/api",
                                        apikey="n3i5idbad2omci5an3cnn7e5m4fmka29tr40t2h0")
# Obtain the API Resource from the connector
wo_set = maxcon.os_resource('MXAPIWODETAIL')
# Specify the select clause
select_clause = maximopyclient.SelectClause(['wonum'])

assets = ['AT100', 'AT101', 'AT102', 'AT103']
# create the WO template json
wo = {'siteid': 'BEDFORD', 'worktype': 'EM'}

for asset in assets:
    # set the assetnum to WO
    wo['assetnum'] = asset
    # create WO
    wo_resp = wo_set.create(wo, select_clause=select_clause)
    print("created workorder " + wo_resp['wonum'])
