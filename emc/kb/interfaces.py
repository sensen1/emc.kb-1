#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema

from emc.kb import _
    
# db insterface
class IModelLocator (Interface):
    """medel table add row"""
    
    def addModel(self):
        "add a model data"
        
    def queryModel(self):
        "query model by search condition"    
    