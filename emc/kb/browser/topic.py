#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from Acquisition import aq_inner
from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from plone.memoize.instance import memoize

from emc.kb.interfaces import IFollowing
from emc.kb.interfaces import IFollowing
from emc.kb.contents.answer import Ianswer
from emc.kb.contents.topic import Itopic
from emc.kb.contents.mentionme import Imentionme
from emc.kb import _

class Itopicview(Interface):
    """
   topic view interface，需要提供关注和取消关注链接
    """
        
    def fetchAllRelatedQuestion(start,size):
        """
        由当前话题作为上下文，返回所有关联到该话题的问题(relatedquestion字段)，返回值为一个obj list,
        需要参考http://pypi.python.org/pypi/z3c.relationfield/0.6.1
        """    
    
    def sortByQuestionModified(brains):
        """
        提供一个问题的brain list，按照问题的修改时间重新排序，返回一个排序后的 brain list
        """    
    def sortByQuestionHotDegree(brains,num):
        """
        提供一个问题的brain list，和一个指定的返回条目的个数参数num,返回一个按问题热度排序的 brain list
        问题热度确认原则是：
        1 该问题下的答案得票数最多
        2 同等得票数的情况下，按最近更新的内容，排在前面
        """    
    def FetchPendingAnswerQuestion(brains,lessthan):
        """
        提供一个问题的brain list，返回一个问题的答案数少于lessthan的问题brain list，并且
        按修改时间排序。
        """                    
    def FetchBestAnswer(brain):
        """
        提供一个问题的brain，返回该问题下得票数最多的答案
        
        """  
    def FetchAuthorPortrait(answerobj):
        """
        提供一个答案,返回该答案作者的头像和作者的homepage
        
        """    
grok.templatedir('templates')

from emc.kb.browser.question import View as baseview
class View(baseview):
    grok.context(Itopic)
    grok.require('zope2.View')
    grok.template('topic_view')
    grok.name('view')
    
    def update(self):
        """
        """
        # Hide the editable-object border
        self.request.set('disable_border', True)
          
    @memoize   
    def catalog(self):
        context = aq_inner(self.context)
        return  getToolByName(context, 'portal_catalog')
         
        
    def isTopicpicAvalable(self,topic=None):
        """判断图片字段是否有效"""
        try:
            if topic is None:
                image = self.context.topicpic.size
            else:
                 image = topic.getObject().topicpic.size
                 
            if image != 0:
                return True
            else:
                return False
        except:
            return False
        
    def transfer2text(self,obj):
        try:
            res = obj.output
            return res
        except:
            return obj  
              
    def fetchAllAnswers(self,qbrain):
        "get all answers in the qbrain question"
        return self.catalog()({'object_provides': Ianswer.__identifier__,
                                 'path': dict(query=qbrain.getPath(),depth=1),
                                 'sort_order': 'reverse',
                                 'sort_on': 'voteNum'})         
        
    @memoize    
    def fetchAllRelatedQuestion(self,start=0,size=10):
        topic = self.context
        intids = getUtility(IIntIds)  
        intid = intids.getId(topic)
        catalog = component.getUtility(ICatalog)
        qlist = sorted(catalog.findRelations({'to_id': intid}))
        if len(qlist)==0:return []        
        startsize = start*size
        endsize = (start+1)*size
        qlistGroup = qlist[startsize:endsize]        
        qlists = []
        for q in qlistGroup:            
            questionobject = self.catalog()({'portal_type': "emc.kb.question",
                                            'id':q.from_object.id,
                                            'sort_order': 'reverse',
                                            'sort_on':'modified'
                                            })
            qlists.append(questionobject[0])          
#         re = self.sortByQuestionModified(qlists)
        return qlists
    
    def sortByQuestionModified(self,brains):
        """
        提供一个问题的brain list，按照问题的修改时间重新排序，返回一个排序后的 brain list
        """
        re = sorted(brains,key=lambda x:x.modified(),reverse=True)
        return  re
     
    def isFollowed(self):
        """判断当前话题是否已被关注,返回boolean"""
        obj = self.context
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()       
        return aobj.available(userid)
    
    def questionIsFollowed(self,qobj):
        """判断指定的问题是否已被关注,返回boolean"""
#        obj = qbrain.getObject()
        aobj = IFollowing(qobj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.available(userid)   
    
    def TopicQuestionNum(self, topicid=None):
        """获取话题下问题数量"""
              
        intids = getUtility(IIntIds)
        
        if topicid == None:
#             topic = self.context
            intid = intids.getId(self.context)
        else:
            topic = self.catalog()({'object_provides':Itopic.__identifier__,
                         'id': topicid
                         })
            intid = intids.getId(topic[0].getObject())

        catalog = component.getUtility(ICatalog)        
        qlist = sorted(catalog.findRelations({'to_id': intid}))
        return len(qlist)
    
    def TopicFollowNum(self, topicid):
        """获取话题关注人数"""
        
        topic = self.catalog()({'object_provides':Itopic.__identifier__,
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

class topicmore(grok.View):
    """AJAX action for updating ratings.
    """
    
    grok.context(Itopic)
    grok.name('topicmore')
    grok.require('zope2.View')            
    
    def render(self):
     
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) 
        nextstart = (formstart+1)*3                
        topic_view = getMultiAdapter((self.context, self.request),name=u"view")
        questionnum = topic_view.TopicQuestionNum()
        topicname = self.context.Title()

        if nextstart>=questionnum :
            ifmore =  1
        else :
            ifmore = 0
            
        braindata = topic_view.fetchAllRelatedQuestion(formstart, 3)
           
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            questionobj = braindata[i]
#             question_view = getMultiAdapter((questionobj, self.request),name=u"view")
            questionUrl = braindata[i].getURL()
            questionTitle = braindata[i].Title
            questionTitle = questionTitle.encode('utf-8')
#             questionid = braindata[i].id.replace('.','_')
            answer = topic_view.fetchAllAnswers(braindata[i])
            answernum = len(answer)
            
            follow = topic_view.questionIsFollowed(braindata[i].getObject())
            if follow:
                followstyle = "display:none;"
                unfollowstyle = "display:inline;"
            else:
                followstyle = "display:inline;"
                unfollowstyle = "display:none;"
            
            if answernum>0:
                firstanswer = answer[0]
                firstanswervoteNum = firstanswer.voteNum
                firstanswerCon = firstanswer.content
                answerhtml = """<div class="boxBody">
                                <div class="boxBodyLeft"><span>%s</span></div>
                                <div class="boxBodyRight">
                                    <div class="content">%s</div>
                                </div>
                            </div>"""%(firstanswervoteNum,firstanswerCon)
            else:
                answerhtml = ""
            
            out = """<div class="qbox hrtop">
                        <div class="boxTitle">
                            <a href="%(qurl)s">%(qtitle)s</a>
                        </div>
                        <div class="answerbox">
                            <div class="boxFoot">
                                    这个问题被添加到
                                <span class="linkcolor">%(topicTitle)s</span>话题•
                                <span>%(answernum)s</span>个答案•
                                <div class="linkcolor">
                                    <span class="follow" style="%(followstyle)s" data-target-url="%(targeturl)s/@@follow">
                        <a class="btn btn-default" href="#">关注问题</a>
                    </span>
                    <span class="unfollow" style="%(unfollowstyle)s" data-target-url="%(targeturl)s/@@unfollow">
                        <a class="btn btn-default" href="#">取消关注</a>                        
                    </span> 
                                </div>
                            </div>
                            %(answerhtml)s
                        </div>
                    </div>""" % dic (
                                     qurl=questionUrl,
                                     qtitle=questionTitle,
                                     topicTitle=topicname,
                                     answernum=answernum,
                                     followstyle=followstyle,
                                     unfollowstyle=unfollowstyle,
                                     answerhtml=answerhtml)
            
            outhtml =outhtml+out
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,
         }
    
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)        