import json
from five import grok
from zope.annotation.interfaces import IAnnotations
from emc.kb.interfaces import ICountStatistics
from emc.kb.interfaces import IClickEvent
from emc.kb.interfaces import ICountAware
from emc.kb.contents.question import Iquestion
from emc.kb.events import CountStatistics
from emc.kb.events import ClickEvent
from zope.component import getMultiAdapter
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IBelowContentTitle
from zExceptions import Forbidden
from zope.interface import implements
from Products.CMFCore.utils import getToolByName


COUNT_KEY = 'emc.kb.answer.count'

class ToCountableObject(grok.Adapter):
    grok.provides(ICountStatistics)
    grok.context(Iquestion)    
    
    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)
        self.key = COUNT_KEY     
    
        if not self.annotations.get(self.key, None):
                self.annotations[self.key] = 1        
    
        
    def setCount(self,num):
        self.annotations[self.key] = num
    
    def getCount(self):
        countNum=self.annotations[self.key]
        return countNum

    def updateCount(self):
        self.annotations[self.key] = self.annotations[self.key] + 1 



#@grok.subscribe(Iquestion, IClickEvent)
def updateCountNumber(obj, event):
    """updatecount"""
    evlute = ICountStatistics(obj)    
    evlute.updateCount()