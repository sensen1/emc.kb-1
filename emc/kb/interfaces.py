#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema

from emc.kb import _
    
class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

# db insterface
class IModelLocator (Interface):
    """medel table add row"""
    
    def addModel(self):
        "add a model data"
        
    def queryModel(self):
        "query model by search condition"
        
class IBranchLocator (Interface):
    """medel table add row"""
    
    def addBranch(self):
        "add a model data"
        
    def queryBranch(self):
        "query model by search condition"

class IFashejLocator (Interface):
    """fashej table add row"""
    
    def add(**kwargs):
        "add a row data"
        
    def query(code):
        "query  by search condition"
        
    def deleteByCode(code):
        "query  by search condition"
        
    def updateByCode(code):
        "query  by search condition"                
        
class IFashetxLocator (IFashejLocator):
    """fashetx table add row"""  

        
class IJieshoujLocator (IFashejLocator):
    """jieshouj table add row"""
    
class IJieshoutxLocator (IFashejLocator):
    """jieshouj table add row"""
    
class ILvboqLocator (IFashejLocator):
    """jieshouj table add row"""
    
class IJieshoujLocator (IFashejLocator):
    """jieshouj table add row"""
    
class IDianxingtxzyzkLocator (IFashejLocator):
    """jieshouj table add row""" 
    
class ITianxianzyzkLocator (IFashejLocator):
    """jieshouj table add row""" 
    
class IJieshoujzkLocator (IFashejLocator):
    """jieshouj table add row""" 
    
class IFashejzkLocator (IFashejLocator):
    """jieshouj table add row""" 
    
                               
                           
    