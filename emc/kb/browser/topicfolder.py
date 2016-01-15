#-*- coding: UTF-8 -*-
from five import grok

from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from emc.kb import  _
from emc.kb.contents.topic import Itopic
from emc.kb.contents.topicfolder import Itopicfolder

grok.templatedir('templates')
class View(grok.View):
    grok.context(Itopicfolder)
    grok.template('topicfolder_view')
    grok.require('zope2.View')
    grok.name('view')
    def update(self):
        self.haveThreads = len(self.fetchAllThreads())>0
    
    @memoize    
    def fetchAllThreads(self):
        """Get all Threads in this forum.
        """

        catalog = getToolByName(self.context, 'portal_catalog')
        return [ dict(url=thread.getURL(),
                      title=thread.Title,
                      author=thread.Creator,
                      createDate = thread.created.strftime('%Y/%m/%d'),)
                 for thread in 
                    catalog({'object_provides':  Itopic.__identifier__,
                             'path': dict(query='/'.join(self.context.getPhysicalPath()),
                                      depth=1),
                             'sort_on': 'sortable_title'})
               ] 