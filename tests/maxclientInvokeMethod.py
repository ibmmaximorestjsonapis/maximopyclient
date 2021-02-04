'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''

import maximopyclient
import ibm_db

maxcon = maximopyclient.MaximoConnector(url="http://localhost:7001/maximo/api",
                                        apikey="n3i5idbad2omci5an3cnn7e5m4fmka29tr40t2h0", session=True)

wo_set = maxcon.os_resource('MXAPIWODETAIL')
select_clause = maximopyclient.SelectClause(['wonum', 'status', 'worktype'])

where_filter = maximopyclient.WhereClause().\
                op_in("wonum", ['1421', '1422'])
# resp = wo_set.fetch_all(where_clause=where_filter, select_clause=select_clause)

resp = wo_set.fetch_first_page(where_clause=where_filter, select_clause=select_clause, page_size=10)
while resp is not None:
    for wo in resp['member']:
        f_wo = wo_set.invoke_method(action_name='createFollowUp', data=wo)
        print("created followup "+f_wo['wonum'])
    if wo_set.has_next_page():
        print("next page")
        resp = wo_set.fetch_next_page()
    else:
        break
