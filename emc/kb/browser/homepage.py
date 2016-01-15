#-*- coding: UTF-8 -*-
from five import grok
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot

from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic
from emc.kb.contents.answer import Ianswer
from emc.kb.contents.questionfolder import Iquestionfolder
from emc.kb.contents.topicfolder import Itopicfolder
from plone.memoize.instance import memoize

from emc.kb import _

from zope.i18n import translate
from zope.i18nmessageid import Message

import time
from time import mktime

from datetime import datetime

JUST_NOW = _(
    u"just now",
    default=u"just now"
             )
MINUTES_AGO = _(
    u"minutes ago",
    default=u"minutes ago"
             )
HOURS_AGO = _(
    u"hours ago",
    default=u"hours ago"
             )
DAYS_AGO = _(
    u"days ago",
    default=u"days ago"
             ) 
A_WEEK_AGO = _(
    u"a week ago",
    default=u"a week ago"
             )
A_MONTH_AGO = _(
    u"a month ago",
    default=u"a month ago"
             )
grok.templatedir('templates')
class View(grok.View):
    grok.context(INavigationRoot)
    grok.template('homepage_view')    
    grok.require('zope2.View')
    grok.name('homepage')
    
    def update(self):
        """
        """
        self.request.set('disable_border', True)
        self.pm = getToolByName(self.context, 'portal_membership')
        if self.pm.isAnonymousUser():
            purl = self.context.absolute_url()
            tourl = purl + "/@@loginview?came_from=%s" % purl
            self.request.response.redirect(tourl)
            
        userobject = self.pm.getAuthenticatedMember()
        self.username = userobject.getId()

        
    def fetchIfollowedTopics(self,size=10):
        """提取我关注的所有话题，返回话题brain list,并按修改时间排序
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        userobject = self.pm.getAuthenticatedMember()
        username = userobject.getId()
        topiclist = list(userobject.getProperty('myfollow'))
        topiclist.reverse()
        topicGroup = topiclist[:size]
        qbrain = []
        for tpc in topicGroup:
            qbrain.append(catalog({'object_provides': Itopic.__identifier__,
                        'id':tpc})[0])
        return qbrain

        
    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj

    def IfollowedTopicNum(self):
        """我关注的话题数量
        """
        userobject = self.pm.getAuthenticatedMember()
        topiclist = userobject.getProperty('myfollow')
        return len(topiclist)
         
    def fetchIfollowedQuestions(self,size=5):
        """提取我关注的所有问题，返回话题brain list,并按修改关注排序
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        userobject = self.pm.getAuthenticatedMember()
        questionlist = list(userobject.getProperty('myfollow'))
        questionlist.reverse()
        questionGroup = questionlist[:size]
        qbrain = []
        for qtn in questionGroup:
            qbrain.append(catalog({'object_provides': Iquestion.__identifier__,
                              'id':qtn})[0])
        return qbrain
        
    def IfollowedQuestionNum(self):
        """我关注的问题数量
        """
        userobject = self.pm.getAuthenticatedMember()
        questionlist = userobject.getProperty('myfollow')
        return len(questionlist)
        
    def fetchMyQustions(self,size=5):
        """提取所有我的问题
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        myquestions = catalog({'portal_type':  'emc.kb.question',
                             'Creator':self.username,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        if size == 0: 
            return myquestions
        elif len(myquestions) <= size:
            return myquestions
        else:
            return myquestions[:size] 
        
    def myQuestionNum(self):
        """我的问题数量
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        myquestions = catalog({'portal_type':  'emc.kb.question',
                             'Creator':self.username,
                             'sort_order': 'reverse',
                             'sort_on': 'modified'})
        return len(myquestions)
        
    def fetchMyAnswers(self,size=3):
        """提取我的答案
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        myanswers = catalog({'object_provides':  Ianswer.__identifier__,
                             'Creator':self.username,
                             'sort_order': 'reverse',                             
                             'sort_on': 'modified'})
        if size == 0: return myanswers
        if len(myanswers) <= size:
            return myanswers
        else:
            return myanswers[:size]
    
    def fetchParentQuestion(self,myanswers):
        obj = myanswers.getObject()
        parentQuestion = obj.getParentNode()
        return parentQuestion
        
    def myAnswerNum(self):
        """我的答案数量
        """
        return len(self.fetchMyAnswers(size=0))
        
    def hotQandA(self,num=10):
        """返回前num个热点问答
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        maxlen = len(catalog({'object_provides': Ianswer.__identifier__}))
        if maxlen > num:
            aa = catalog({'object_provides': Ianswer.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'voteNum',
                             'sort_limit': num})
        else:
            aa = catalog({'object_provides': Ianswer.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'voteNum'})

        return aa
        
    def hotTopics(self,num=10):
        """返回前num个热点话题
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        
        maxlen = len(catalog({'object_provides': Itopic.__identifier__}))
        if maxlen > num:
            return catalog({'object_provides': Itopic.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'topicscore',
                             'sort_limit': num})
        else:
            return catalog({'object_provides': Itopic.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'topicscore'})
    
    def getQuestionFolder(self):
        context = aq_inner(self.context)
        qfc = getToolByName(context, 'portal_catalog')
        questionfolder = qfc({'object_provides': Iquestionfolder.__identifier__})
        if len(questionfolder) >0:
            qfpath = questionfolder[0].getURL()
        else:
            qfpath = None            
        return qfpath
    
    def getTopicFolder(self):
        context = aq_inner(self.context)
        tfc = getToolByName(context, 'portal_catalog')
        topicfolder = tfc({'object_provides': Itopicfolder.__identifier__})
        if len(topicfolder) > 0:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath
    
    def friendlydatetime(self,answercatalog):
        """根据创建时间，返回一个类似于：
        3天前，
        2小时前,...
        的友好时间显示        
        """         
        fmt='%Y/%m/%d %H:%M:%S'
        date = answercatalog.created.Date()
        times = answercatalog.created.Time()
        x = date + ' ' + times
        dx = time.strptime(x,"%Y/%m/%d %X")
        dy=datetime.fromtimestamp(mktime(dx))
        dz = datetime.now()
        mNum = ((dz-dy).seconds)/60
        hNum = ((dz-dy).seconds)/3600
        dNum=(dz-dy).days
        if dNum == 0:
            if hNum == 0:
                if mNum == 0:
                    message = translate(Message(JUST_NOW),
                                context=self.request)
                    return message
                else:
                    message = translate(Message(MINUTES_AGO),
                                context=self.request)
                    return str(mNum) + message
            else:
                    message = translate(Message(HOURS_AGO),
                                context=self.request)
                    return str(hNum)+ message
        elif dNum <= 7:
                message = translate(Message(DAYS_AGO),
                                context=self.request)
                return str(dNum) + message
        elif dNum > 7 and dNum <= 30:
            message = translate(Message(A_WEEK_AGO),
                                context=self.request)  
            
            return message
        else:
            message = translate(Message(A_MONTH_AGO),
                                context=self.request)            
            return message
