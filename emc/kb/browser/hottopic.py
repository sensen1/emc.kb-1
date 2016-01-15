#-*- coding: UTF-8 -*-
import time
from five import grok
from zope.interface import Interface
from emc.kb.contents.topicfolder import Itopicfolder
from emc.kb.contents.topic import Itopic
from emc.kb.utility import topicdate


from plone.app.layout.navigation.interfaces import INavigationRoot
from AccessControl.SecurityManagement import getSecurityManager
from Products.CMFCore.utils import getToolByName

from zope.component import getMultiAdapter

from emc.kb import _

class IhotTopic(Interface):
    """
    hotanswer view interface
    """
            
    def fetchHotTopic(days):
        """ 获取前面10个热门话题，会有一个参数加在链接后面，没有参数是全部，参数是7返回7天内的，
        参数是30返回30天以内的，需要话题名和链接，不用分页，返回dict类型 """
        
grok.templatedir('templates')
class hotTopic(grok.View):
    grok.context(INavigationRoot)
    grok.template('hottopic_view')    
    grok.require('zope2.View')    
    grok.name('hottopic')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        self.catalog = getToolByName(self.context, 'portal_catalog')

#    def currentDateNum(self):
#        st2 = self.request["QUERY_STRING"]
#        """默认为7天"""
#        if len(st2) == 0:
#            limit = 7
#        else:
#            st = st2.split("=")
#            try:
#                 limit = int(st[1])
#            except:
#                 limit = 0
#        return limit

    def fetchAllTopicfolder(self):
        """提取所有topic folder,返回一个brain list"""
        
#        query = dict(object_provides=Itopicfolder.__identifier__)
        return self.catalog({'object_provides': Itopicfolder.__identifier__})
    
    def fetchAllTopic(self,brain):
        """传入一个话题文件夹的brain,提取该话题文件夹下所有话题"""
        alltopics = self.catalog({'object_provides': Itopic.__identifier__,
                              'path': dict(query=brain.getPath(),depth=1),                                     
                             'sort_on': 'modified'})        
        return alltopics

        
        
    def fetchHotTopic(self,limit=10):
        """ 获取前面10个热门话题，会有一个参数加在链接后面，没有参数是全部，参数是7返回7天内的，参数是30返回30天以内的，
        需要话题名和链接，不用分页，返回dict类型 """
#        days = self.currentDateNum()
            
#        ago = topicdate.getdayofday(-days)
#        agotoday =  "%s-%s-%s" % (ago.year,ago.month,ago.day)
       
        topiclist = self.catalog({'object_provides': Itopic.__identifier__,
                              'sort_order': 'reverse',                                     
                              'sort_on': 'topicscore',
                              'sort_limit':limit})
        return topiclist

       