'''
Created on Aug 2, 2020

@author: AnamitraBhattacharyy
'''

class SelectClause:
    '''
    classdocs
    '''

    def __init__(self, props=["*"], object_name=None, relation=None, relation_os=None, all_header_props=False):
        self.props = props
        self.relation = relation
        self.relation_os = relation_os
        self.all_header_props = all_header_props
        self.related_select_clauses = None
        self.object_name = object_name
        if self.all_header_props:
            self.props = ["_allheaderprops_"]
            
    def add(self, select_clause):
        if self.all_header_props:
            return 
        if self.related_select_clauses is None:
            self.related_select_clauses = []
        self.related_select_clauses.append(select_clause)
        
    def to_string(self):
        clause = ""
        if self.props is None and self.related_select_clauses is None:
            return None
        if self.relation is not None:
            if self.relation_os is None:
                clause = "rel."+self.relation+"{"
            else:
                clause = "rel." + self.relation + self.relation_os + "{"
        elif self.object_name is not None:
            clause = self.object_name + "{"
        else:    
            clause = ""
        if self.props is not None:
            for elem in self.props:
                clause += elem+","
        if self.related_select_clauses is not None:
            for related_clause in self.related_select_clauses:
                clause += related_clause.to_string()
        clause = clause[:(len(clause)-1)]
        if self.relation is not None or self.object_name is not None:
            clause = clause + "}"
        return clause
        
    def params(self):
        params = {}
        params['oslc.select'] = self.to_string()
        print(params['oslc.select'])
        return params
        