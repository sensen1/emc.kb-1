#-*- coding: UTF-8 -*-
from five import grok
import json
import time
from time import mktime
from datetime import datetime
from zope.i18n import translate
from zope.i18nmessageid import Message

from emc.kb.contents.answer import Ianswer
from emc.kb.contents.question import Iquestion
from emc.kb.contents.questionfolder import Iquestionfolder
from emc.kb.interfaces import IFollowing

from AccessControl.SecurityManagement import getSecurityManager
from zope.interface import Interface
from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot

from zope.interface import Interface
from zope.component import getMultiAdapter
from plone.app.discussion.interfaces import IConversation
from plone.memoize.instance import memoize

from emc.kb import  _

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
class Iquestion(Interface):
    """
    hotanswer view interface
    """
    def getuseranswer(self):
        """获取用户回答过到所有问题答案"""
    def isFollowed(self,brain):
        """brain问题catalog判断当前问题是否已被当前用户关注,返回boolean"""
    def fetchAnswerNum(self,myquestion):
        """myquestion问题catalog类型获取指定问题下的答案个数"""
        
class Imyanswer(Interface):
    """
    hotanswer view interface
    """
        
    def timeToToday(self):
        """返回答案创建时间距离今天的日期，一周前，几天前到格式"""    
        
grok.templatedir('templates')
from emc.kb.browser.question import View as baseview
class myquestion(baseview):
    grok.context(INavigationRoot)
    grok.template('question_view')
    grok.require('zope2.View')    
    grok.name('myquestion')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)    
        userobject = self.mp().getAuthenticatedMember()
        self.username = userobject.getId()        
        self.haveMyQuestions = bool(self.myQuestionNum >0)
    
    @memoize
    def mp(self):
        return getToolByName(self.context,'portal_membership')    
    @memoize
    def catalog(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog    
    
    @memoize
    def myQuestionNum(self):
        """获取我的问题数目"""               
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        myquestions =  self.catalog()()({'portal_type':  'emc.kb.question',
                     'Creator':username})
        return len(myquestions)
    
    def myAnswerNum(self):
        """获取我的答案数目"""
        myanswers =  self.catalog()({'object_provides':  Ianswer.__identifier__,
                             'Creator':self.username})
        return len(myanswers)
        
    def isFollowed(self,brain):
        """判断当前问题是否已被当前用户关注,返回boolean"""
        obj = brain.getObject().getParentNode()
        aobj = IFollowing(obj)         
        return aobj.available(self.username)
    
    @memoize
    def getuseranswer(self):
        """获取用户回答过到所有问题的答案"""
        
        userobject = self.mp().getAuthenticatedMember()
        return self.catalog()({'object_provides':  Ianswer.__identifier__,
                              'Creator': userobject.getId()
                              })

    @memoize
    def affiliatedtopics(self,qbrain):
        """需要返回一个问题的相关话题""" 
        topic = qbrain.getObject()        
        intids = getUtility(IIntIds)  
        intid = intids.getId(topic)
        catalog = component.getUtility(ICatalog)        
        qlist = sorted(catalog.findRelations({'from_id': intid}))
        qlists = []

        for q in qlist: 
            qlists.append(q.to_object)
        re = sorted(qlists,key=lambda x:x.modified(),reverse=True)                 
        return re 
               
    def fetchAnswerNum(self,myquestion):
        """获取指定问题下的答案个数"""
#        obj = myquestion.getObject()
        
        answerNum = len(self.catalog()({'object_provides':  Ianswer.__identifier__,
                             'path': dict(query=myquestion.getPath(),
                                      depth=1)}))
        return answerNum

    def fetchMyQuestions(self, start=0, size=3):       
        
        userobject = sefl.mp().getAuthenticatedMember()
        username = userobject.getId()
        myquestions =  self.catalog()({'portal_type':  'emc.kb.question',
                             'Creator':username,
                             'sort_on': 'created',
                             'sort_order': 'reverse',
                             'b_start': start,
                             'b_size': size})
        return myquestions
    
    def isFollowed(self,qbrain):
        """给定问题qbrain,判断该该问题是否已被关注,返回boolean"""
        obj = qbrain.getObject()
        aobj = IFollowing(obj)
        userobject = self.mp().getAuthenticatedMember()
        userid = userobject.getId()         
        return aobj.available(userid)
    
    def fetchMyAnswer(self, start=0, size=11): 
        myanswers =  self.catalog()({'object_provides':  Ianswer.__identifier__,
                             'Creator':self.username,
                             'sort_on': 'sortable_title',
                             'b_start': start,
                             'b_size': size,})
        return myanswers     

  
class myquestionmore(grok.View):
    """AJAX action for updating ratings.
    """
    
    grok.context(INavigationRoot)
    grok.name('myquestionmore')
    grok.require('zope2.View')            
    
    def render(self):    
       
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst)*3 
        nextstart = formstart+3
                
        myquestion_view = getMultiAdapter((self.context, self.request),name=u"myquestion")
        myquestionnum = myquestion_view.myQuestionNum()
        
        if nextstart>=myquestionnum :
            ifmore =  1
        else :
            ifmore = 0
        
        braindata = myquestion_view.fetchMyQuestions(formstart, 3)   
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            questionUrl = braindata[i].getURL()
            questionTitle = braindata[i].Title
            answerNum = myquestion_view.fetchAnswerNum(braindata[i])
            questionid = braindata[i].id
            topics = myquestion_view.affiliatedtopics(braindata[i])
            tnum = len(topics)
            follow = myquestion_view.isFollowed(braindata[i])
            if follow:
                followstyle1 = "display:none;"
                followstyle2 = "display:inline;"
            else:
                followstyle1 = "display:inline;"
                followstyle2 = "display:none;"
            
            
            ajaxaction1 = self.context.absolute_url() + "/@@ajax-follow"
            ajaxaction2 = self.context.absolute_url() + "/@@ajax-unfollow"
            
            out = """<div class="qbox hrbottom">
                        <div class="boxTitle">
                            <a href="%s">%s</a>
                        </div>
                        <div class="boxFoot">
                            <a href="%s"><span>%s</span><span>答案</span></a>
                        &nbsp;•&nbsp;
                        
                    <span id="ajax-question-follow-%s" style="%s" question-follow="%s">
                        <a class="followjq" href="#">关注问题</a>
                        <input type="text" style="display:none" value="%s" />
                    </span>
                    <span id="ajax-question-unfollow-%s" style="%s" question-unfollow="%s">
                        <a class="unfollowjq" href="#">取消关注</a>
                        <input type="text" style="display:none" value="%s" />
                    </span>"""%(questionUrl,questionTitle,questionUrl,answerNum,questionid,followstyle1,ajaxaction1,questionid,questionid,followstyle2,ajaxaction2,questionid);
            if tnum >3:                
                topiclist = ""
                for j in range(3):
                    topicUrl = topics[j].absolute_url()
                    topicTitle = topics[j].title
                    topiclist = topiclist+"""<span><a href="%s">%s</a>.</span>"""%(topicUrl,topicTitle)
                topiclist = topiclist.encode('utf-8')
                topiclist = topiclist+"""等<span class="linkcolor">%s</span>话题"""%(tnum)                
                relatetopic = """•&nbsp;涉及到%s</div></div>"""%(topiclist)
                
            elif tnum>0:                
                topiclist = ""
                for j in range(tnum):
                    topicUrl = topics[j].absolute_url()
                    topicTitle = topics[j].title
                    topiclist = topiclist+"""<span><a href="%s">%s</a>.</span>"""%(topicUrl,topicTitle)
                topiclist = topiclist.encode('utf-8')
                relatetopic = """•&nbsp;涉及到%s话题</div></div>"""%(topiclist)
            else:
                relatetopic = """</div></div>"""
                
            outhtml =outhtml+out+relatetopic
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,
         }
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)

     
class myanswer(myquestion):
    grok.context(INavigationRoot)
    grok.template('answer_view')     
    grok.require('zope2.View')    
    grok.name('myanswer')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        userobject = self.mp().getAuthenticatedMember()        
        self.username = userobject.getId()
        self.haveMyAnswer = bool(self.myAnswerNum>0)    
        
    def getcommentnum(self,brain = None):
        """获取问题直接评论"""
        if brain is None:
            conversation = IConversation(self.context)
        else:
            conversation = IConversation(brain.getObject())
        return conversation.total_comments
        
    def myQuestionNum(self):
        """获取我的问题数目"""
        myquestions =  self.catalog()({'portal_type':  'emc.kb.question',
                     'Creator':self.username,
                     'sort_on': 'modified'})
        return len(myquestions)
    
    def myAnswerNum(self):
        """获取我的答案数目"""
        
        
        userobject = self.mp().getAuthenticatedMember()        
        username = userobject.getId()
        myanswers =  self.catalog()({'object_provides':  Ianswer.__identifier__,
                             'Creator':username,
                             'sort_on': 'sortable_title'})
        return len(myanswers)
    
    def isFollowed(self,brain):
        """判断当前问题是否已被当前用户关注,返回boolean"""
        
        userobject = self.mp().getAuthenticatedMember()        
        username = userobject.getId()
        obj = brain.getObject().getParentNode()
        aobj = IFollowing(obj)       
        return aobj.available(username)
    
    def timeToToday(self,answercatalog):
        """返回答案创建时间距离今天的日期，一周前，几天前到格式，字符串"""
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
        
    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj

    def fetchParentQuestion(self,myanswer):
        obj = myanswer.getObject()
        parentQuestion = obj.getParentNode()
        return parentQuestion    

    def fetchMyAnswer(self, start=0, size=10): 
        
        
        userobject = self.mp().getAuthenticatedMember()        
        username = userobject.getId()
        myanswers =  self.catalog()({'object_provides':  Ianswer.__identifier__,
                             'Creator':username,
                            'sort_order': 'reverse',
                             'sort_on': 'modified',
                             'b_start': start,
                             'b_size': size})
        return myanswers
    
    def fetchMyQuestions(self, start=0, size=10):
        myquestions =  self.catalog()({'portal_type':  'emc.kb.question',
                             'Creator':self.username,
                             'sort_on': 'modified',
                             'b_start': start,
                             'b_size': size})
        return myquestions
    
class myanswermore(grok.View):
    """AJAX action for updating ratings.
    """
    
    grok.context(INavigationRoot)
    grok.name('myanswermore')
    grok.require('zope2.View')

            
    
    def render(self):
       
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst)*3 
        nextstart = formstart+3                
        myanswer_view = getMultiAdapter((self.context, self.request),name=u"myanswer")
        myanswernum = myanswer_view.myAnswerNum()
        
        if nextstart>=myanswernum :
            ifmore =  1
        else :
            ifmore = 0
        
        braindata = myanswer_view.fetchMyAnswer(formstart, 3)
      
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            answerUrl = braindata[i].getURL()
            parentQuestion = myanswer_view.fetchParentQuestion(braindata[i])
            questionTitle = parentQuestion.title
            questionTitle = questionTitle.encode('utf-8')
            voteNum = braindata[i].voteNum
            answerCon = braindata[i].content
            questionid = parentQuestion.id
            answerid = braindata[i].id
            timetotoday = myanswer_view.timeToToday(braindata[i])
            timetotoday = timetotoday.encode('utf-8')
            commentnum = myanswer_view.getcommentnum(braindata[i])
            follow = myanswer_view.isFollowed(braindata[i])
            if follow:
                followstyle1 = "display:none;"
                followstyle2 = "display:inline;"
            else:
                followstyle1 = "display:inline;"
                followstyle2 = "display:none;"
            
            if commentnum>0:
                commentstyle1 = "display:inline;"
                commentstyle2 = "display:none;"
            else:
                commentstyle1 = "display:none;"
                commentstyle2 = "display:inline;"
            
            ajaxaction1 = self.context.absolute_url() + "/@@ajax-follow"
            ajaxaction2 = self.context.absolute_url() + "/@@ajax-unfollow"
                
            out = """<div class="qbox hrbottom">
                        <div class="boxTitle">
                            <a href="%s">%s</a>
                        </div>
                        <div class="boxBody">
                            <div class="boxBodyLeft"><span>%s</span></div>
                            <div class="boxBodyRight">
                                <div class="content">%s</div>
                            </div>
                        </div>
                        <div class="boxFoot">
                            <span id="ajax-question-follow-%s%s" style="%s" question-follow="%s">
                                <a class="followjq" href="#">关注</a>
                                <input type="text" style="display:none" id="%s" value="%s" />
                            </span>
                            <span id="ajax-question-unfollow-%s%s" style="%s" question-unfollow="%s">
                                <a class="unfollowjq" href="#">取消关注</a>
                                <input type="text" style="display:none" id="%s" value="%s" />
                            </span>
                            &nbsp;•&nbsp;
                            <span>%s</span>
                        </div>
                    </div>"""%(answerUrl,questionTitle,voteNum,answerCon,questionid,answerid,followstyle1,ajaxaction1,answerid,questionid,questionid,answerid,followstyle2,ajaxaction2,answerid,questionid,timetotoday)
            
            outhtml =outhtml+out
            
            data = {                
                'outhtml': outhtml,
                'ifmore':ifmore,
             }
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)