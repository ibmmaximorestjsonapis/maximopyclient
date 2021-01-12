'''
Created on Jul 31, 2020

@author: AnamitraBhattacharyy
'''

class OrderByClause:
    '''
    classdocs
    '''
    def __init__(self):
        print("start where clause")
        self.filter_params = {}

    def add_clause(self, attr, asc):
        order_by_clause = ""
        if 'oslc.orderBy' not in self.filter_params:
            order_by_clause = ""
        else:
            order_by_clause = self.filter_params['oslc.orderBy']
            order_by_clause += ","
        
        if asc==True:
            order_by_clause += "+"+attr.lower()
        else:
            order_by_clause += "-"+attr.lower()
        
        self.filter_params['oslc.orderBy'] = order_by_clause
    
    def params(self):
        return self.filter_params
