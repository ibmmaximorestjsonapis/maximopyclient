'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''


import maximopyclient
import json

maxcon = maximopyclient.MaximoConnector(url="http://localhost:7001/maximo/api", apikey="n3i5idbad2omci5an3cnn7e5m4fmka29tr40t2h0", session=True)

wo_set = maxcon.os_resource('MXAPIWODETAIL')
select_clause = maximopyclient.SelectClause(['wonum','status','worktype'])

where_filter = maximopyclient.WhereClause().\
    op_equals('status', 'WAPPR').\
    op_equals('worktype', 'EM').\
    op_in("asset.assettype",['GEN','FORKLIFT'])
#resp = wo_set.fetch_all(where_clause=where_filter, select_clause=select_clause)

resp = wo_set.fetch_first_page(where_clause=where_filter,select_clause=select_clause, page_size=10)
while resp is not None:
    for wo in resp['member']:
        wo['status'] = 'APPR'
        wo_set.merge(wo)
    if wo_set.has_next_page():
        resp = wo_set.fetch_next_page()
    else:
        break




