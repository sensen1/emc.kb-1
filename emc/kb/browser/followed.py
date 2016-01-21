#-*- coding: UTF-8 -*-
from five import grok
import json
from zope.interface import Interface
from plone.memoize.instance import memoize

from emc.kb.contents.questionfolder import Iquestionfolder
from emc.kb.contents.topicfolder import Itopicfolder
from emc.kb.contents.question import Iquestion
from emc.kb.contents.topic import Itopic
from emc.kb.contents.answer import Ianswer

from zope.interface import Interface
from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope.component import getMultiAdapter

from plone.app.layout.navigation.interfaces import INavigationRoot
from AccessControl.SecurityManagement import getSecurityManager
from plone.app.layout.globals.context import ContextState
from emc.kb.interfaces import IFollowing
from emc.kb import  _

class Iquestionfollowed(Interface):
    """
    questionfollowed view interface

    """
    def fetchquestionsIfollowed(start=0,size=20):
        """当前用户关注的所有问题，返回问题brains""" 
            

    def IFollowedTopicNum():
        """当前用户关注话题数目"""                 
    def IFollowedAllTopic(start=0,size=20):
        """当前用户关注所有话题，返回话题brains"""         
    def fetchaffiliatedtopics(self,questionobject):
        """取得问题的相关话题，最多返回三个相关话题，需要话题的标题，URL，返回dict型。"""    

    def affiliatedtopicsNum(self,questionobject):
        """需要返回一个相关话题数目""" 
        
    def affiliatedtopics():
        """需要返回一个问题的相关话题""" 
        
class Itopicfollowed(Interface):
    """
    topicfollowed view interface

    """
    def IFollowedQuestionNum():
        """当前用户关注话题数目""" 
    def IFollowedAllQuestion(start=0,size=20):
        """当前用户关注所有话题，返回话题brains"""   
        
grok.templatedir('templates')
class questionfollowed(grok.View):
    grok.context(INavigationRoot)
    grok.template('questionfollowed_view')    
    grok.require('zope2.View')    
    grok.name('questionfollowed')
    
    def update(self):
        
        self.haveQuestions = bool(self.IFollowedQestionNum())>0
        self.questionsnum = self.IFollowedQestionNum()
        self.topicsnum = self.IFollowedTopicNum()
        
    def isFollowed(self,qbrain):
        """给定问题qbrain,判断该该问题是否已被关注,返回boolean"""
        obj = qbrain.getObject()
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()                
        return aobj.available(userid)
    
    @memoize
    def IFollowedTopicNum(self):
        """当前用户关注话题数目""" 
        return len(self.IFollowedAllTopic(start=0, size=0))
    
    @memoize
    def IFollowedQestionNum(self):
        """当前用户关注问题数目""" 
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        
        questionlist = list(userobject.getProperty('myfollowquestion'))
        catalog = getToolByName(self.context, 'portal_catalog')
        
        return len(catalog({'object_provides': Iquestion.__identifier__,
                        'UID':questionlist}))
                
    def fetchquestionsIfollowed(self, start=0, size=10):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        
        questionlist = list(userobject.getProperty('myfollowquestion'))
        catalog = getToolByName(self.context, 'portal_catalog')
        
        questionlist.reverse()
        startsize = start*size
        endsize = (start+1)*size
        questionGroup = questionlist[startsize:endsize]
        qbrain = []        
        for tpc in questionGroup:
            qbrain.append(catalog({'object_provides': Iquestion.__identifier__,
                        'UID':tpc})[0])
        return qbrain
    
    def IFollowedAllTopic(self, start=0, size=3):
        "关注的话题"
        
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        topiclist = userobject.getProperty('myfollowtopic')
        catalog = getToolByName(self.context, 'portal_catalog')
        if (start==0 and size==0):
            return catalog({'object_provides':  Itopic.__identifier__,
                        'UID':topiclist,
                        'sort_on': 'modified',
                        'sort_order': 'reverse'})        
        return catalog({'object_provides':  Itopic.__identifier__,
                        'UID':topiclist,
                        'b_start': start,
                        'b_size': size})
        
    def questionsIfollowedIndex(self, qbrain):
        catalog = getToolByName(self.context, 'portal_catalog')
        
        num = len(catalog({'object_provides': Ianswer.__identifier__,
                                       'path': dict(query=qbrain.getPath(),depth=1)}))
        return num

    @memoize
    def affiliatedtopics(self,qbrain):
        """需要返回一个问题的相关话题数目""" 
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
   

   
  
class questionfollowedmore(grok.View):
    """AJAX action for load more.
    """
    
    grok.context(INavigationRoot)
#     grok.template('topicfollowed_view')
    grok.name('questionfollowedmore')
    grok.require('zope2.View')

    def render(self):
    
#         self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) 
        nextstart = (formstart+1)*3
                
        questionfollowed_view = getMultiAdapter((self.context, self.request),name=u"questionfollowed")
        questionfollowednum = questionfollowed_view.IFollowedQestionNum()
        
        if nextstart>=questionfollowednum :
            ifmore =  1
        else :
            ifmore = 0
        
        # a batch 
        braindata = questionfollowed_view.fetchquestionsIfollowed(formstart, 3)     
      
        
        outhtml = ""
        brainnum = len(braindata)
        # question brains loop
        for i in range(brainnum):
            questionUrl = braindata[i].getURL()
            questionTitle = braindata[i].Title
            answerNum = questionfollowed_view.questionsIfollowedIndex(braindata[i])
            questionid = braindata[i].id.replace('.','_')
            topics = questionfollowed_view.affiliatedtopics(braindata[i])
            tnum = len(topics)
            # is followed ?
            follow = questionfollowed_view.isFollowed(braindata[i])
            if follow:
                followstyle = "display:none;"
                unfollowstyle = "display:inline;"
            else:
                followstyle = "display:inline;"
                unfollowstyle = "display:none;"
            
            out = """<div class="qbox hrbottom">
                        <div class="boxTitle">
                            <a href="%(qurl)s">%(qtitle)s</a>
                        </div>
                        <div class="boxFoot">
                            <a href="%(qurl)s"><span>%(answers)s</span><span>答案</span></a>
                        &nbsp;•&nbsp;
                        
                    <span class="follow" style="%(followstyle)s" data-target-url="%(targeturl)s/@@follow">
                        <a class="btn btn-default" href="#">关注问题</a>
                    </span>
                    <span class="unfollow" style="%(unfollowstyle)s" data-target-url="%(targeturl)s/@@unfollow">
                        <a class="btn btn-default" href="#">取消关注</a>                        
                    </span>""" % dict (qurl=questionUrl,
                                  qtitle=questionTitle,
                                  answers=answerNum,
                                  followstyle=followstyle,
                                  unfollowstyle=unfollowstyle,
                                  targeturl=questionUrl)
            if tnum >3:                
                topiclist = ""
                for j in range(3):
                    topicUrl = topics[j].absolute_url()
                    topicTitle = topics[j].title
                    topiclist = topiclist +"""<span><a href="%s">%s</a>.</span>"""%(topicUrl,topicTitle)
                topiclist = topiclist.encode('utf-8')
                topiclist = topiclist +"""等<span class="linkcolor">%s</span>话题"""%(tnum)                
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
 
class topicfollowed(grok.View):
    grok.context(INavigationRoot)
    grok.template('topicfollowed_view')
    grok.require('zope2.View')    
    grok.name('topicfollowed')
    
    def update(self):
        
        self.haveTopics = bool(self.fetchtopicsIfollowed())>0
        self.questionsnum = self.IFollowedQuestionNum()        
        self.topicsnum = self.IFollowedTopicNum()
    
    def isFollowed(self,tbrain):
        """给定话题tbrain,判断该话题是否已被关注,返回boolean"""
        obj = tbrain.getObject()
        aobj = IFollowing(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        
        return aobj.available(userid)
    
    def IFollowedTopicNum(self):
        """当前用户关注话题数目""" 
       
        return len(self.Followedtopiclist())
    
    @memoize
    def Followedtopiclist(self):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        fwtlist = list(userobject.getProperty('myfollowtopic'))
        return fwtlist
    
    @memoize
    def Followedquestionlist(self):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        fwqlist = list(userobject.getProperty('myfollowquestion'))
        return fwqlist             
        
   
    def IFollowedQuestionNum(self):
        """当前用户关注问题数目""" 
        return len(self.Followedquestionlist())
    
    def IFollowedAllQuestion(self, start=0, size=10):
        

        fwqlist = self.Followedquestionlist()
        catalog = getToolByName(self.context, 'portal_catalog')
        if (start==0 and size==0):
            return catalog({'object_provides':  Iquestion.__identifier__,
                        'UID':fwqlist,
                        'sort_on': 'modified',
                        'sort_order': 'reverse'})        
        return catalog({'object_provides':  Iquestion.__identifier__,
                        'UID':fwqlist,
                        'sort_on': 'modified',
                        'sort_order': 'reverse',
                        'b_start': start,
                        'b_size': size})        
    def IFollowedAllTopic(self, start=0, size=2):       

        topiclist = self.Followedtopiclist()

        catalog = getToolByName(self.context, 'portal_catalog')
        if (start==0 and size==0):
            return catalog({'object_provides':  Itopic.__identifier__,
                        'UID':topiclist,
                        'sort_on': 'modified',
                        'sort_order': 'reverse'})        
        return catalog({'object_provides':  Itopic.__identifier__,
                        'UID':topiclist,
                        'sort_on': 'modified',
                        'sort_order': 'reverse',
                        'b_start': start,
                        'b_size': size}) 
    def fetchtopicsIfollowed(self, start=0, size=2):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        topiclist = list(userobject.getProperty('myfollowtopic'))
    
        catalog = getToolByName(self.context, 'portal_catalog')
        topiclist.reverse()
        startsize = start*size
        endsize = (start+1)*size
        topicGroup = topiclist[startsize:endsize]
        qbrain = []
        for tpc in topicGroup:
            qbrain.append(catalog({'object_provides': Itopic.__identifier__,
                        'UID':tpc})[0])
        aa = qbrain
        return aa
        
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

class topicfollowedmore(grok.View):
    """AJAX action for updating ratings.
    """
    
    grok.context(INavigationRoot)
    grok.name('topicfollowedmore')
    grok.require('zope2.View')            
    
    def render(self):
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) 
        nextstart = (formstart+1)*2
                
        topicfollowed_view = getMultiAdapter((self.context, self.request),name=u"topicfollowed")
        topicfollowednum = topicfollowed_view.IFollowedTopicNum()
        
        if nextstart>=topicfollowednum :
            ifmore =  1
        else :
            ifmore = 0
        
        braindata = topicfollowed_view.fetchtopicsIfollowed(formstart, 2)    
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            havaTopicpic = topicfollowed_view.isTopicpicAvalable(braindata[i])
            topicobj = braindata[i].getObject()
            topicadapt = getMultiAdapter((topicobj, self.request),name=u"images")                      
            
            if havaTopicpic:
                thumb = topicadapt.scale('topicpic',width=64, height=64)
                imgtag = """<img src="%s" width=%s height=%s />""" % \
                (thumb.url,thummb.width,thumb.height)               
            else:
                imgtag = """<img src="++resource++emc.kb/topicdefault.gif" />"""                
            topicUrl = braindata[i].getURL()
            topicDescription = braindata[i].Description
            topicTitle = braindata[i].Title
            follow = topicfollowed_view.isFollowed(braindata[i])
            if follow:
                followstyle = "display:none;"
                unfollowstyle = "display:inline;"
            else:
                followstyle = "display:inline;"
                unfollowstyle = "display:none;"
            
            out = """<div class="qbox hrbottom">
                        <div class="boxTopicBody">
                            <div class="boxBodyLeft" style="(%fact)s">
                                <a href="%(turl)s">(%imgtag)s</a>
                            </div>                           
                            <div class="boxBodyRight">
                                <div>
                                    <a href="%(turl)s">%(ttitle)s</a>                                    
                    <span class="follow" style="%(followstyle)s" data-target-url="%(targeturl)s/@@follow">
                        <a class="btn btn-default" href="#">关注话题</a>
                    </span>
                    <span class="unfollow" style="%(unfollowstyle)s" data-target-url="%(targeturl)s/@@unfollow">
                        <a class="btn btn-default" href="#">取消关注</a>                        
                    </span>                                    
                                </div>
                                <div class="boxBodyContent">%(description)s</div>
                            </div>
                        </div>
                    </div>"""% dict  (turl = topicUrl,
                                  ttitle = topicTitle,
                                  imgtag = imgtag,
                                  followstyle = followstyle,
                                  unfollowstyle = unfollowstyle,
                                  targeturl = questionUrl,
                                  description = topicDescription)
            outhtml =outhtml+out
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,
         }
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)   