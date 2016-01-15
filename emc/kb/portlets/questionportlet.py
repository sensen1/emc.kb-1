#import random

from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter
from zope import component
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from emc.kb.interfaces import ICountStatistics
from emc.kb.contents.question import Iquestion
from emc.kb.interfaces import ICountAware
from emc.kb import  _


class IQuestionPortlet(IPortletDataProvider):

    count = schema.Int(
            title=_(u"Number of related question to display"),
            description=_(u"Maximum number of related question to show"),
            required=True,
            default=10,
        )            
class Assignment(base.Assignment):
    implements(IQuestionPortlet)

    def __init__(self, count=10):
        self.count = count

#     @property
#     def title(self):
#         return _(u"Related questions")

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('questionportlet.pt')
    
    @property
    def available(self):
        return len(self._data()) > 0
#    def getcount(self):
#
#
#        context = self.context        
#        if ICountAware.providedBy(context):
#            pass
#        else:
#            return 0
        
#        coutableobj = ICountStatistics(context)
#        num = coutableobj.getCount()      
#        
#        event.notify(ClickEvent(context))
#        return num

    def relatedquestions(self):
#        
#        for relatedquestion in self._data():
#            import pdb
#            pdb.set_trace()
#            yield dict(title=relatedquestion.title,
#                   url=relatedquestion.absolute_url
#                    )            

            re = [dict(title=relatedquestion.title,
                       url=relatedquestion.absolute_url,
                      ) for relatedquestion in self._data()]
            return re
    @memoize
    def _data(self):    
        question=self.context
        intids = getUtility(IIntIds)  
        intid = intids.getId(question)
        catalog = component.getUtility(ICatalog)        
        topiclist = sorted(catalog.findRelations({'from_id': intid}))
        topiclists=[]
        
        for tc in topiclist: 
            topiclists.append(tc.to_object)

       
        if len(topiclists) == 0:
           return topiclists[:]
        elif len(topiclists) ==1: 
            topic=topiclists[0]
            intid = intids.getId(topic)
            catalog = component.getUtility(ICatalog)        
            questionlist = sorted(catalog.findRelations({'to_id': intid}))
            relatedquestions=[]
            for q in questionlist:
                catalog = getToolByName(self.context, 'portal_catalog')
                questionobject = catalog({'portal_type': "emc.kb.question",
                                                'id':q.from_object.id
                                                })
                relatedquestions.append(questionobject[0].getObject()) 
            if question in relatedquestions:
                relatedquestions.remove(question)

            return relatedquestions[0:10]
        
        else:
            topic1=topiclists[0]
            intid = intids.getId(topic1)
            catalog = component.getUtility(ICatalog)     
            questionlist1 = sorted(catalog.findRelations({'to_id': intid}))        
            questionlist1s=[]
            for q in questionlist1: 
                catalog = getToolByName(self.context, 'portal_catalog')
                questionobject = catalog({'portal_type': "emc.kb.question",
                                                'id':q.from_object.id
                                                })
                questionlist1s.append(questionobject[0].getObject())  
            if question in questionlist1s:
                questionlist1s.remove(question)           
            
            topic2=topiclists[1]
            intid = intids.getId(topic2)
            catalog = component.getUtility(ICatalog)        
            questionlist2 = sorted(catalog.findRelations({'to_id': intid}))                   
            questionlist2s=[]
            for q in questionlist2: 
                catalog = getToolByName(self.context, 'portal_catalog')
                questionobject = catalog({'portal_type': "emc.kb.question",
                                                'id':q.from_object.id
                                                })
                questionlist2s.append(questionobject[0].getObject()) 
            if  question in questionlist2s:
                questionlist2s.remove(question)
                
            for que in questionlist1s[:5] :
                   if que in questionlist2s[:5]:
                       questionlist2s.remove(que)         
            relatedquestions=questionlist1s[:5]+questionlist2s[:5]

            return relatedquestions
            


class AddForm(base.AddForm):
    form_fields = form.Fields(IQuestionPortlet)
    label = _(u"Add related question portlet")
    description = _(u"This portlet displays related question.")


    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IQuestionPortlet)
    label = _(u"Edit recent related question")
    description = _(u"This portlet displays related question.")
    
    