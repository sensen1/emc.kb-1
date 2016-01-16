#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements

from emc.kb import kb_session
from emc.kb.mapping_db import Model
from emc.kb.interfaces import IModelLocator

from emc.kb import MessageFactory as _

class ModelLocator(grok.GlobalUtility):
    implements(IModelLocator)
    
    def Addmodel(self,modelId,xhdm,xhmc):
        """parameters db model table"""
        model = Model()
        model.id = modelId
        model.xhdm = xhdm
        model.xhmc = xhmc

        kb_session.add(model)
        try:
            kb_session.commit()
        except:
            kb_session.rollback()
            raise