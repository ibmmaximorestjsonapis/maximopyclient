'''
Created on Jul 28, 2020

@author: AnamitraBhattacharyy
'''
from datetime import date, datetime, time


class WhereClause:
    
    def __init__(self):
        print("start where clause")
        self.filter_params = {}
        
    def params(self):
        return self.filter_params
    
    def __where_for_anding(self):
        curr_where = ""
        if 'oslc.where' not in self.filter_params:
            curr_where = ""
        else:
            curr_where = self.filter_params['oslc.where']
            curr_where += " and "
        return curr_where
    
    def __val_to_token(self, val):
        tok = ""
        if(type(val) == str):
            tok = '"'+val+'"'
        elif(type(val)==int or type(val) == float):     
            tok = str(val)
        elif(type(val)==date or type(val) == datetime or type(val) == time):    
            tok = '"'+val.isoformat()+'"'
        return tok

    def saved_query(self, saved_query_name):
        print("start where clause " + saved_query_name)
        self.filter_params["savedQuery"] = saved_query_name
        
    def op_mode_or(self, is_or):
        if is_or:
            self.filter_params["opmodeor"] = "1"
        else:
            del self.filter_params["opmodeor"]
    
    def op_in(self, attr, values):
        curr_where = self.__where_for_anding()
        in_clause = ""
        for val in values: 
            in_clause += self.__val_to_token(val) + ","
        in_clause = in_clause[:len(in_clause)-1]
        in_clause = "["+in_clause+"]"
        curr_where += attr + " in " + in_clause
        self.filter_params['oslc.where'] = curr_where
        
    def op_equals(self, attr, val):
        curr_where = self.__where_for_anding()
        eq_clause = attr+"="+self.__val_to_token(val)
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where

    def op_not_equals(self, attr, val):
        curr_where = self.__where_for_anding()
        eq_clause = attr+"!="+self.__val_to_token(val)
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where
        
    def op_greater_than(self, attr, val):
        curr_where = self.__where_for_anding()
        eq_clause = attr+">"+self.__val_to_token(val)
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where
    
    def op_greater_than_equals(self, attr, val):
        curr_where = self.__where_for_anding()
        eq_clause = attr+">="+self.__val_to_token(val)
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where

    def op_less_than_equals(self, attr, val):
        curr_where = self.__where_for_anding()
        eq_clause = attr+"<="+self.__val_to_token(val)
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where

    def ops_less_than(self, attr, val):
        curr_where = self.__where_for_anding()
        eq_clause = attr+"<"+self.__val_to_token(val)
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where

    def op_not_in(self, attr, values):
        curr_where = self.__where_for_anding()
        inClause = ""
        for val in values: 
            inClause += val+","
        inClause = inClause[:len(inClause)-1]
        inClause = '"['+inClause+']"'
        curr_where += attr + " != " + inClause
        self.filter_params['oslc.where'] = curr_where
        
    def op_is_not_null(self, attr):
        curr_where = self.__where_for_anding()
        eq_clause = attr+"="+'"*"'
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where
        
    def filter_domain(self, domain_name, site, org):
        self.filter_params['_fd'] = domain_name
        if site is not None:
            self.filter_params['_fdsite'] = site
        if org is not None:
            self.filter_params['_fdorg'] = org

    def domain_internal_where(self, attr, eq, values):
        in_clause = attr
        for val in values: 
            in_clause += val+","
        in_clause = in_clause[:len(in_clause)-1]
        op = "="
        if eq == False:
            op = "!="
        self.filter_params['domaininternalwhere'] = attr + op + '[' + in_clause + ']'

    def op_is_null(self, attr):
        curr_where = self.__where_for_anding()
        eq_clause = attr+"!="+'"*"'
        curr_where += eq_clause
        self.filter_params['oslc.where'] = curr_where

    def search_terms(self, terms, attrs):
        search_terms = ""
        for term in terms: 
            search_terms += '"'+term+'",'
        search_terms = search_terms[:len(search_terms)-1]
        self.filter_params['oslc.searchTerms'] = search_terms
        search_attrs = ""
        if attrs is not None:
            for attr in attrs: 
                search_attrs += '"'+attr+'",'
            self.filter_params['searchAttributes'] = search_attrs
