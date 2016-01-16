#-*- coding: UTF-8 -*-
import time
from five import grok
from Acquisition import aq_parent
from emc.kb.contents.answer import Ianswer
from emc.kb.utility import topicdate

from zope.interface import Interface

from plone.app.layout.navigation.interfaces import INavigationRoot
from AccessControl.SecurityManagement import getSecurityManager
from Products.CMFCore.utils import getToolByName
#from zope.i18n.interfaces import ITranslationDomain
#from zope.component import queryUtility
from zope.i18n import translate
from zope.i18nmessageid import Message

from zope.component import getMultiAdapter

from emc.kb import _

ALL_DAY = _(
    u"all day",
    default=u"all day"
             )

class Ihotanswer(Interface):
    """
    hotanswer view interface
    """
        
    def todayDate():
        """返回今天的日期，年月日格式"""    
        
    def weekagoDate():
        """返回一周前的日期，年月日格式"""    
        
    def monthagoDate():
        """返回一个月前的日期，年月日格式""" 
                   
    def fetchHotAnswer():
        """ 获取前面10个热门答案，以答案的赞成数为首要排序条件，次要排序条件为答案的创建时间，返回为catalog类型 """

    def fetchdatedisplay():
        """  默认返回为 一周前的日子-今天的日期，
        参数为30，返回30天前的日期-今天的日期，
        参数为0，返回ALL,
        返回为字符串类型 """
        
    def fetchParentQuestion(self,answerbarin):
        """根据答案取得问题的标题""" 
       

grok.templatedir('templates')
class hotanswer(grok.View):
    grok.context(INavigationRoot)
    grok.template('hotanswer_view')    
    grok.require('zope2.View')    
    grok.name('hotanswer')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        self.haveHotAnswer = len(self.fetchHotAnswer())>0
        
    def currentDateNum(self):
        st2 = self.request["QUERY_STRING"]
        """默认为7天"""
        if len(st2) == 0:
            limit = 7
        else:
            st = st2.split("=")
            try:
                 limit = int(st[1])
            except:
                 limit = 0
        return limit
    @property
    def membership(self):
        context = aq_inner(self.context)
        return getToolByName(context,'portal_membership')
    
    def todayDate(self):
        """返回今天的日期，年月日格式"""
        today = time.strftime("%Y年%m月%d日",time.localtime())
        
        return today
    
    def weekagoDate(self):
        """返回一周前的日期，年月日格式"""
        weekago = topicdate.getdayofday(-7)
        translation_service = getToolByName(self.context,'translation_service')
        weekagotoday = translation_service.translate(
                                                  'a_week_ago_date',
                                                  domain='emc.kb',
                                                  mapping={'year': weekago.year,'month':weekago.month,
                                                           'day':weekago.day},
                                                  context=self.context,
                                                  default=u"${year}年${month}月${day}日")
        return weekagotoday
    
    def monthagoDate(self):
        """返回一个月前的日期，年月日格式""" 
        monthago = topicdate.get_today_month(-1)
        translation_service = getToolByName(self.context,'translation_service')
        monthagotoday = translation_service.translate(
                                                  'a_mounth_ago_date',
                                                  domain='emc.kb',
                                                  mapping={'year': monthago.year,'month':monthago.month,
                                                           'day':monthago.day},
                                                  context=self.context,
                                                  default=u"${year}年${month}月${day}日")
        
        return monthagotoday
    
    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj
                      
        
    def fetchHotAnswer(self,limit=20):
        """ 获取前面10个热门答案，以答案的赞成数为首要排序条件，次要排序条件为答案的创建时间，返回为catalog类型 """
        """默认为7天"""
        limit = self.currentDateNum()
        catalog = getToolByName(self.context, 'portal_catalog')
        if limit == 0:
            abrains = catalog({'object_provides': Ianswer.__identifier__,
                               'totalNum': {'query' : 1,'range': 'min'},
                             'sort_order': 'reverse',
                             'sort_on': 'totalNum'})
        else:
            abrains = catalog({'object_provides': Ianswer.__identifier__,
                             'sort_order': 'reverse',
                             'totalNum': {'query' : 1,'range': 'min'},
                             'sort_on': "totalNum",
                             'sort_limit': limit})
        """先票数后时间排序"""
        re = sorted(abrains,key=lambda x:(x.totalNum,x.modified),reverse=True)
        return re
    
    def fetchdatedisplay(self):
        """  默认返回为 一周前的日子-今天的日期，
        参数为30，返回30天前的日期-今天的日期，
        参数为0，返回ALL,
        返回为字符串类型 """
        
#        st2 = self.request["QUERY_STRING"]
#        
#        """默认为7天"""
#        if len(st2) == 0:
#            days = 7
#        else:
#            st = st2.split("=")
#            try:
#                 days = int(st[1])
#            except:
#                 return _(u"All")
#            if days == 0:
#                return _(u"All")
        days = self.currentDateNum()
        if days == 0:
            message = translate(Message(ALL_DAY),
                                context=self.request)
            return message
        
        ago = topicdate.getdayofday(-days)
        today = unicode(time.strftime("%Y年%m月%d日",time.localtime()),"utf-8")
        translation_service = getToolByName(self.context,'translation_service')
        agotoday = translation_service.translate(
                                                  'ago_date',
                                                  domain='emc.kb',
                                                  mapping={'year': ago.year,'month':ago.month,
                                                           'day':ago.day},
                                                  context=self.context,
                                                  default=u"${year}年${month}月${day}日")
        return "%s----%s"%(agotoday,today)
    
    def fetchParentQuestion(self,answerbarin):
        """根据答案取得问题的标题"""
        questionobject = aq_parent(answerbarin.getObject())
        return questionobject.title
        
    def GetAuthorInfoAnswer(self,hotanswer):
        """根据答案id获取作者相关信息，包括包含链接，描述，头像"""
        catalog = getToolByName(self.context, 'portal_catalog')
        query = dict(object_provides=Ianswer.__identifier__,id=hotanswer.id)
        answerobject = catalog(query)[0].getObject()
        pm = getToolByName(self.context, 'portal_membership')
        userobject=pm.getMemberById(answerobject.Creator())
        username = userobject.getProperty('fullname')
        authorinfo = {}
        try:
            authorinfo['username'] = username
            authorinfo['homepage'] = pm.getHomeUrl(userobject.getId()) + '/feedsfolder'
            authorinfo['description'] = userobject.getProperty('description')
            authorinfo['portrait'] = userobject.getPersonalPortrait(userobject.getId())
        except:
            authorinfo = {"username":'testuser',"homepage":'http://test.com',"description":'testuser',
                          "portrait":'defaultUser.png'}
        return authorinfo