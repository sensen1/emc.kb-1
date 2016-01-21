#-*- coding: UTF-8 -*-
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from emc.kb.interfaces import IFollowing

from emc.kb.contents.topic import Itopic
from emc.kb.contents.answer import Ianswer
from emc.kb.contents.question import Iquestion

from zope import component
from zope.intid import IntIds
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zc.relation.interfaces import ICatalog

class Isearchview(Interface):
    
    def fetchTopics(self):
        """获取符合搜索词的话题，返回标题、描述、图片"""
        
    def TopicQuestionNum(self, topicid):
        """获取话题关注人数及包含问题数量"""
        
    def TopicFollowNum(self, topicid):
        """获取话题关注人数"""
        
    def Topicisfollowed(self, topicid):
        """话题是否被当前用户关注"""
    
    def fetchQuestions(self):
        """获取符合搜索词的问题，返回标题"""

    def QuestionAnswerNum(self, questionid):
        """获取问题含答案数量"""
        
    def Questionfollowed(self, questionid):
          """获取问题关注人数"""
          
    def Questionisfollowed(self, questionid):
        """问题是否被当前用户关注"""
        
grok.templatedir('templates')
class View(grok.View):
    grok.context(INavigationRoot)
    grok.template('search_view') 
    grok.require('zope2.View')
    grok.name('search')
    
    def update(self):
        self.textbox = self.receive()
    
    def fetchallsearch(self,start=0,size=10):
        """获取符合搜索词的话题，返回标题、描述、图片"""
        data = self.receive()
        if len(data) == 0: return
        catalog = getToolByName(self.context, 'portal_catalog')
        
        searchlist = catalog({'SearchableText': '*'+data+'*',
                            'sort_order':'reverse',
                            'sort_on':'Date',
                            'b_start': start,
                            'b_size': size
                         })
        return searchlist
    
    def isObjecttype(self,obrain):
        """判断是否为问题对象str{1:话题,2:问题}"""
        ob = obrain.getObject()
        """话题对象"""
        if Itopic.providedBy(ob):
            return 1
        """问题对象"""
        if Iquestion.providedBy(ob):
            return 2
        
        return 3

    def isTopicpicAvalable(self,topic):
        """判断图片字段是否有效"""
        try:
            image = topic.getObject().topicpic.size
            if image != 0:
                return True
            else:
                return False
        except:
            return False
    
    def TopicQuestionNum(self, topicid):
        """获取话题下问题数量"""
        catalog = getToolByName(self.context, 'portal_catalog')
        topic = catalog({'object_provides':Itopic.__identifier__,
                         'id': topicid
                         })
        intids = getUtility(IIntIds)
        intid = intids.getId(topic[0].getObject())
        catalog = component.getUtility(ICatalog)        
        qlist = sorted(catalog.findRelations({'from_id': intid}))
        return len(qlist)
    
    def TopicFollowNum(self, topicid):
        """获取话题关注人数"""
        catalog = getToolByName(self.context, 'portal_catalog')
        topic = catalog({'object_provides':Itopic.__identifier__,
                      'id': topicid
                         })
        aobj = IFollowing(topic[0].getObject())
        return aobj.followerNum
    
    def Topicisfollowed(self,topic):
        """判断当前话题是否已被关注,返回boolean"""
        obj = topic.getObject()
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()       
        return aobj.available(userid)
    
#    def fetchQuestions(self):
#        """获取符合搜索词的问题，返回标题"""
#        data = self.receive()
#        if len(data) == 0: return
#        catalog = getToolByName(self.context, 'portal_catalog')
#        questionlist = catalog({'object_provides':Iquestion.__identifier__,
#                                'Title': '%'+data+'%',
#                                'sort_order':'reverse',
#                                'sort_on':'Date'
#                         })
#        return questionlist
    
#    def fetchTopicQuestions(self,topicobject):
#        """获取指定话题下符合搜索词的问题，返回标题"""
#        data = self.receive()
#        if len(data) == 0: return
#        
#        intids = getUtility(IIntIds)  
#        intid = intids.getId(topicobject)
#        catalog = component.getUtility(ICatalog)
#        qlist = sorted(catalog.findRelations({'to_id': intid}))
#        if len(qlist)==0:return []
#        qlists = []
#        for q in qlist: 
#            qlists.append(q.from_object.id)
#            
#        catalog = getToolByName(self.context, 'portal_catalog')
#        re = catalog({'object_provides':Iquestion.__identifier__,
#                                      'Title': '%'+data+'%',
#                                      'id': qlists
#                                        })    
#        return re
    
    def QuestionAnswerNum(self,questionid):
        """获取问题下答案数量"""
        catalog = getToolByName(self.context, 'portal_catalog')
        question = catalog({'object_provides':Iquestion.__identifier__,
                            'id': questionid
                         })
        answerlist = catalog({'object_provides':Ianswer.__identifier__,
                          'sort_order': 'reverse',
                         'sort_on': 'voteNum',
                         'path': question[0].getPath()
                         })
        return len(answerlist)
    
    def Questionfollowed(self, questionid):
        """获取问题关注人数"""
        catalog = getToolByName(self.context, 'portal_catalog')
        question = catalog({'object_provides':Iquestion.__identifier__,
                      'id': questionid
                         })
        aobj = IFollowing(question[0].getObject())
        return aobj.followerNum
    
    def Questionisfollowed(self,question):
        """判断当前问题是否已被关注,返回boolean"""
        obj = question.getObject()
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.available(userid)  

        
    def receive(self):
        data = self.request.form
        if len(data) == 0 or data['form.SearchableText'] == "":
            return "请输入搜索词"
        else:
            return data['form.SearchableText']