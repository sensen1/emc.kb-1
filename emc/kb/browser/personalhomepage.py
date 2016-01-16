#-*- coding: UTF-8 -*-
from five import grok
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from emc.kb.contents.feedsfolder import Ifeedsfolder
from emc.kb.contents.feed import Ifeed
from emc.kb.contents.question import Iquestion
from emc.kb.contents.answer import Ianswer
from emc.kb.interfaces import IFollowing

from zope import component
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zc.relation.interfaces import ICatalog

grok.templatedir('templates')
class View(grok.View):
    grok.context(Ifeedsfolder)
    grok.template('personalhomepage_view') 
    grok.require('zope2.View')
    grok.name('view')
    def update(self):
        """"""
        self.request.set('disable_border', True)
        self.feedsNum = len(self.fetchAllFollowedNewThings())
        self.havefeeds = self.feedsNum>0
        
    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj

    def isFollowed(self,brain):
        """提供一个问题的brain,判断当前问题是否已被关注,返回boolean"""
        obj = brain.getObject()
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()            
        return aobj.available(userid)
        
    def fetchAllFollowedNewThings(self,size=0,start=20):
        """从我关注的新增事务文件家中feedsfolder，获取所有新增问题
        或新增答案的问题brains，
        返回一个brain list，每个brain为feed对象的brain
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        feedbrain = catalog({'portal_type':"emc.kb.feed",
                             'path': '/'.join(context.getPhysicalPath())
                             })
        return feedbrain
    def fetchFeedType(self,brain):
        """提供一个feed brain，返回一个整型值标明该feed类型：
            1 -话题下新增问题
    2 - 话题下新增回答
    3 - 问题下新增回答
        """
        obj=brain.getObject()
        types = int(obj.type)
        return types
        
    def fetchAuthorInfo(self,brain):
        """根据对象brain获取该对象作者相关信息
        包括：
        作者头像，链接，名称等
        """

        pm = getToolByName(self.context, 'portal_membership')
#        import pdb
#        pdb.set_trace()        
        userobject=pm.getMemberById(brain.Creator)
        authorinfo = {}
        authorinfo['username'] = userobject.getId()
        authorinfo['homepage'] = pm.getHomeUrl()
        authorinfo['description'] = userobject.getProperty('description')
        authorinfo['portrait'] = userobject.getPersonalPortrait()
        return authorinfo
    def fetchQobjByid(self,feedbrain):
        """根据feed对象的brain，返回问题对象的brain
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        qbrain = catalog({'object_provides':Iquestion.__identifier__,
                          'id':feedbrain.id})
        return qbrain[0]
        
    def fetchRlatedTopic(self,qbrain):
        """根据问题brain获取相应话题，返回话题topic object list
        """
        intids = getUtility(IIntIds)  
        intid = intids.getId(qbrain.getObject())
        catalog = component.getUtility(ICatalog)        
        tbrainlist = sorted(catalog.findRelations({'from_id': intid}))
        re = [ p.to_object for p in tbrainlist]
        return re
        
    def fetchAnswerNumByQuestion(self,qbrain):
        """根据问题brain返回该问题下的答案数
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        answerlist = catalog({'object_provides':Ianswer.__identifier__,
                              'path': '/'.join(qbrain.getPath())
                              })
        return len(answerlist)
        
    def isFollowedByQuestion(self,qbrain):
        """根据问题brain判断该问题是否被当前用户关注，返回布尔值
        """
        obj = (self.context).getParentNode()
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        
        return aobj.available(userid)
        
    def fetchnewestAnswerByQuestion(self,qbrain):  
        """根据问题brain获取该问题下最新的一个答案
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        answerlist = catalog({'object_provides': Ianswer.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'modified',
                             'path': '/'.join(qbrain.getPath())
                             })
        if len(answerlist) == 0:
            return []
        else:
            newest = answerlist[0]
        return newest